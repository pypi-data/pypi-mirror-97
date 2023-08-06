#!/usr/bin/env python
"""
    A simple CLI client for Endpoint services.

    This CLI requires the python package `rl`, which it dynamically
    loads in `launch_cli()`. To install this package, along with its
    dependencies on a Debian-based Linux system (e.g. Ubuntu), do the
    following:

    sudo apt install python-dev python3-dev
    sudo apt install libtinfo-dev
    sudo apt-get install libreadline-dev
    pip install rl

"""
from __future__ import print_function

import sys
import os
import argparse
import logging
import signal
import time
import json
from threading import Thread
try:
    import queue
except ImportError:
    import Queue as queue
from collections import OrderedDict
import socket
from getpass import getpass

import websocket

from loreiosdk.utils.command_argparse import CommandArgumentParser,\
    CommandArgumentError, CommandArgumentMessage

__author__ = 'Bill Chickering'

# params
READLINE_HIST_FILE = '.spyglass_history'
CLI_PROMPT = 'spyglass> '
CLI_MESSAGE = 'enter `help` for a list of endpoint commands'
QUEUE_WAIT = 0.5  # seconds

# colored format for TTY (i.e. console)
tty_fmt = ('%(asctime)s %(process)d (%(thread)d) %(levelname)s '
           '\033[0;34m%(name)s (%(lineno)d)\033[0m '
           '%(funcName)s(): \033[0;32m%(message)s\033[0m')

# plain text format for files
pln_fmt = ('%(asctime)s %(process)d (%(thread)d) %(levelname)s '
           '%(name)s (%(lineno)d) '
           '%(funcName)s(): %(message)s')

# globals
logger = logging.root
seqno = 0
spyglass_commands = OrderedDict()
write_file = None
timex_cmds = False
time_send = 0
blocking = False
unblock = False


def setup_logging():
    """Configure logging."""
    logger.handlers = []
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    if sys.stderr.isatty():
        stream_handler.setFormatter(logging.Formatter(tty_fmt))
    else:
        stream_handler.setFormatter(logging.Formatter(pln_fmt))
    logger.addHandler(stream_handler)


def get_argparser():
    """Define and parse options."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('url', type=str, help='endpoint URL')
    parser.add_argument('--session_id', type=str, help='session ID')
    parser.add_argument('--timex', action='store_true',
                        help='time execution of endpoint commands')
    parser.add_argument('-e', '--editing_mode', type=str, default='vi',
                        choices=['emacs', 'vi'], help='editing mode')
    parser.add_argument('-t', '--trace', action='store_true',
                        help='enable websocket tracing')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='produce debugging output')
    return parser


def get_prompt(prompt=CLI_PROMPT):
    """Returns CLI prompt."""
    return '-->%d %s' % (seqno, prompt)


def show_cli_message():
    """Print cli message."""
    print(CLI_MESSAGE)


def clear_readline():
    """Clear readline buffer from display."""
    sys.stdout.write(
        '\r' + ' '*(len(rl.readline.get_line_buffer()) + 2) + '\r'
    )


# ====================
# spyglass commands
# ====================


def help_command(ws, *args):
    """show list of spyglass commands"""
    parser = CommandArgumentParser(
        prog='help', description=help_command.__doc__
    )
    pargs, _ = parser.parse_known_args(args)
    command_descs = OrderedDict()
    for key, value in spyglass_commands.items():
        if value['forward']:
            desc = ' '.join([value['function'].__doc__, '(forwarded)'])
        else:
            desc = value['function'].__doc__
        command_descs[key] = desc
    message = 'list of spyglass commands:\n'
    message += '(enter a command with the -h option for details)\n'
    fmt_str = '{0:>16}:  {1:<}'
    message += '\n'.join(
        [fmt_str.format(n, d) for n, d in command_descs.items()]
    )
    message += '\n'
    print(message)
    return 'help ' + ' '.join(args)


def quit_command(ws, *args):
    """quit spyglass"""
    # this command is merely a dummy used by help
    # quit logic is implemented within run_cli()
    parser = CommandArgumentParser(
        prog='quit', description=quit_command.__doc__
    )
    pargs, _ = parser.parse_known_args(args)
    return('quit ' + ' '.join(args))


def status_command(ws, *args):
    """show spyglass state info"""
    parser = CommandArgumentParser(
        prog='status', description=status_command.__doc__
    )
    pargs, _ = parser.parse_known_args(args)
    if write_file is not None:
        print('write_file: %s' % write_file.name)
    return 'status ' + ' '.join(args)


def readf_command(ws, *args):
    """read command arg(s) from file"""
    parser = CommandArgumentParser(
        prog='readf', description=readf_command.__doc__
    )
    parser.add_argument('filename', type=str, help='name of input file')
    parser.add_argument(
        'command',
        nargs='+',
        type=str,
        help='command text (contents of file will be appended)',
        metavar=''
    )
    pargs, _ = parser.parse_known_args(args)
    with open(pargs.filename, 'r') as input_file:
        input_str = input_file.read()
    return ' '.join(pargs.command) + ' ' + input_str


def writef_command(ws, *args):
    """configure spyglass to write results to file"""
    global write_file
    parser = CommandArgumentParser(
        prog='writef', description=writef_command.__doc__
    )
    parser.add_argument('filename', nargs='?', type=str, default=None,
                        help='name of output file (omit to close file)')
    pargs = parser.parse_args(args)
    if write_file is not None:
        write_file.close()
    if pargs.filename is None:
        write_file = None
    else:
        try:
            write_file = open(pargs.filename, 'w')
        except IOError:
            write_file = None
            raise CommandArgumentError('IOError, failed to open file')


def timex_command(ws, *args):
    """time execution of endpoint commands"""
    global timex_cmds
    parser = CommandArgumentParser(
        prog='timex', description=timex_command.__doc__
    )
    parser.add_argument('mode', choices=['on', 'off'], help='mode')
    pargs = parser.parse_args(args)
    if pargs.mode == 'on':
        timex_cmds = True
    else:
        timex_cmds = False


def auth_command(ws, *args):
    """enter username and password and send to endpoint"""
    parser = CommandArgumentParser(
        prog='auth', description=auth_command.__doc__
    )
    parser.add_argument('username', type=str, help='username')
    pargs = parser.parse_args(args)
    password = getpass(get_prompt('enter password> '))
    return 'auth %s %s' % (pargs.username, password)


def setup_spyglass_commands():
    """Setup spyglass_commands."""
    global spyglass_commands
    spyglass_commands = OrderedDict([
        ('auth', {'function': auth_command, 'forward': True}),
        ('help', {'function': help_command, 'forward': True}),
        ('quit', {'function': quit_command, 'forward': True}),
        ('status', {'function': status_command, 'forward': True}),
        ('readf', {'function': readf_command, 'forward': True}),
        ('writef', {'function': writef_command, 'forward': False}),
        ('timex', {'function': timex_command, 'forward': False}),
    ])


# ==========================


def get_endpoint_commands(ws):
    """Retrieve endpoint commands."""
    global seqno
    logger.debug('CALLING ws.send()')
    ws.send('%d help --raw' % seqno)
    logger.debug('RETURNED from ws.send()')
    logger.debug('CALLING ws.recv()')
    result_json = ws.recv()
    logger.debug('RETURNED from ws.recv()')
    logger.debug('result_json = %s' % result_json)
    result = json.loads(result_json)
    assert(result['seqno'] == seqno)
    if 'message' in result:
        raise ValueError('Failed to retrieve endpoint commands. '
                         'ERROR: %s' % result['message'])
    seqno += 1
    return [tup[0] for tup in result['data']]


def listen(ws, queues):
    """Handle results from endpoint."""
    timex = 0
    while True:
        logger.debug('Listener listening on socket')
        try:
            logger.debug('CALLING ws.recv()')
            result_json = ws.recv()
            logger.debug('RETURNED from ws.recv()')
            if timex_cmds:
                timex = time.time() - time_send
            result = json.loads(result_json)
        except socket.error as e:
            if str(e) == '[Errno 35] Resource temporarily unavailable':
                continue
            break
        except:
            break
        clear_readline()
        logger.debug('write_file = %s' % str(write_file))
        if write_file:
            print('%d<-- (written to %s)' % (result['seqno'], write_file.name))
        if (('data' not in result or result['data'] is None) and
                'message' in result):
            # write 'message', which is simple text
            output = result['message']
            if not write_file:
                print('%d<-- %s' % (result['seqno'], result['message']))
        else:
            # write JSON-serialized 'data'
            output = json.dumps(result['data'])
            if not write_file:
                print(result_json)
        if timex_cmds:
            clear_readline()
            print('timex: %.3f seconds' % timex)
        if write_file is not None:
            # write output to file
            write_file.write(output)
            write_file.write('\n')
            write_file.flush()
        sys.stdout.write(get_prompt() + rl.readline.get_line_buffer())
        sys.stdout.flush()

        logger.debug('Listener writes %d' % result['seqno'])
        queues[1].put(result['seqno'])


def run_cli(ws, queues, session_id=None):
    """Run command line interface."""
    global seqno, time_send, unblock, blocking

    def sigint_handler(signal, frame):
        global unblock
        unblock = True
        if not blocking:
            print('')
            print('(enter `quit` to shutdown spyglass)')
            print(get_prompt())
            sys.stdout.flush()

    signal.signal(signal.SIGINT, sigint_handler)

    show_cli_message()
    init = False
    while True:
        if not init:
            init = True
            if session_id is not None:
                name = 'session'
                message = ' '.join([name, session_id])
                print(''.join([get_prompt(), message]))
                time_send = time.time()
                logger.debug('CALLING ws.send()')
                ws.send('%d %s' % (seqno, message))
                logger.debug('RETURNED from ws.send()')
                read_message = False
            else:
                read_message = True
        else:
            read_message = True
        if read_message:
            clear_readline()
            try:
                message = raw_input(get_prompt())
            except:
                message = input(get_prompt())
            toks = message.split()
            if len(toks) == 0:
                continue
            name = toks[0]
            if name in spyglass_commands.keys():
                logger.debug('handling spyglass_command %s' % name)
                try:
                    message = spyglass_commands[name]['function'](
                        ws,
                        *toks[1:]
                    )
                except (CommandArgumentMessage, CommandArgumentError) as e:
                    if e.message:
                        print(e.message)
                # TODO: refactor code to avoid redundancy
                except (socket.error,
                        websocket.WebSocketConnectionClosedException):
                    print('Connection closed. Shutting down spyglass. . .',
                          file=sys.stderr)
                    break
                if not spyglass_commands[name]['forward']:
                    continue
            try:
                time_send = time.time()
                logger.debug('CALLING ws.send()')
                ws.send('%d %s' % (seqno, message))
                logger.debug('RETURNED from ws.send()')
            except (socket.error,
                    websocket.WebSocketConnectionClosedException):
                print('Connection closed. Shutting down spyglass. . .',
                      file=sys.stderr)
                break
        toks = message.split()
        if len(toks) == 0:
            continue
        name = toks[0]
        logger.debug('CLI reading queue')
        blocking = True
        while True:
            if name == 'quit':
                break
            try:
                sn = queues[0].get(True, QUEUE_WAIT)
            except queue.Empty:
                if unblock:
                    unblock = False
                    break
                else:
                    continue
            logger.debug('CLI reads %d' % sn)
            if sn == seqno:
                break
        blocking = False
        if name == 'quit' and '-h' not in toks and '--help' not in toks:
            print('Shutting down spyglass. . .')
            break
        seqno += 1


def launch_cli(ws, editing_mode, session_id=None):
    """Launch CLI."""
    global rl

    # must dynamically import rl
    # otherwise, extra junk to stdout for one-off commands
    rl = __import__('rl')

    # setup spyglass_commands
    setup_spyglass_commands()

    # configure readline
    logger.debug('editing_mode = %s' % editing_mode)
    rl.completer.parse_and_bind('set editing-mode %s' % editing_mode)
    readline_hist_file = os.path.join(os.environ['HOME'],
                                      READLINE_HIST_FILE)
    if os.path.isfile(readline_hist_file):
        rl.history.read_file(readline_hist_file)

    # configure tab completion
    commands = list(spyglass_commands.keys())
    commands += get_endpoint_commands(ws)

    def complete_command(text):
        """Return commands matching `text`."""
        for command in commands:
            if command.startswith(text):
                yield command

    rl.completer.completer = rl.generator(complete_command)
    rl.completer.parse_and_bind('tab: complete')

    # create queues for inter-thread communication
    q1 = queue.Queue()
    q2 = queue.Queue()

    # launch listener
    thread = Thread(target=listen, args=(ws, [q2, q1]))
    thread.start()

    # run command line interface
    run_cli(ws, [q1, q2], session_id=session_id)

    # close socket
    ws.close()

    # join threads
    thread.join()

    # close write file
    if write_file is not None:
        write_file.close()

    # save readline history
    rl.history.write_file(readline_hist_file)


def main():
    global timex_cmds, time_send

    # setup logging
    setup_logging()

    # parse args
    pargs = get_argparser().parse_args()

    # set logging level
    if pargs.debug:
        logger.setLevel(logging.DEBUG)

    if pargs.timex:
        timex_cmds = True

    # connect to server
    websocket.enableTrace(pargs.trace)
    print('Connecting to: %s' % pargs.url, file=sys.stderr)
    try:
        time_send = time.time()
        ws = websocket.create_connection(pargs.url)
        if timex_cmds:
            timex = time.time() - time_send
            print('timex: %s seconds' % timex, file=sys.stderr)
    except socket.error:
        logger.exception('Connection to server refused')
        sys.exit(1)

    if pargs.session_id is not None:
        logger.debug('session_id = %s' % pargs.session_id)

    launch_cli(ws, pargs.editing_mode, session_id=pargs.session_id)


if __name__ == "__main__":
    main()
