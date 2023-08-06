import json
import logging
from time import sleep

try:
    import thread
except ImportError:
    import _thread as thread
import websocket

__author__ = 'Maurin Lenglart'

logger = logging.root

MAX_RETRIES = 5

STATUS = ['DONE', 'IN_PROGRESS']


class LoreException(Exception):
    pass


class Spyglass:
    _url = None
    _ws = None
    _username = None
    _password = None

    dataset_id = None
    seqno = 0

    def __init__(self, url, username, password, dataset_id=None):
        self._url = url
        self._username = username
        self._password = password
        self.dataset_id = dataset_id
        self.connect()

    def connect(self):
        websocket.enableTrace(False)
        self._ws = websocket.WebSocketApp(self._url,
                                          on_open=self._on_open,
                                          on_message=self._on_message,
                                          on_error=self._on_error,
                                          on_close=self._on_close)
        self._connecting = True
        self.connected = False
        thread.start_new_thread(self._ws.run_forever, ())
        self.results = {}
        # wait for connection and auth
        while self._connecting:
            sleep(0.1)

        if not self.connected:
            raise Exception("Could not connect")

        if self.dataset_id:
            self.cmd("session", self.dataset_id)

    def _on_open(self):
        def _auth(*args):
            self._ws.send(
                '{} auth {} {}'.format(self.seqno, self._username,
                                       self._password))
            while True:
                sleep(0.1)
                if self.seqno in self.results:
                    if self.results[self.seqno]['message'] == 'Success':
                        self.connected = True
                    else:
                        self.connected = False
                    self._connecting = False
                    break

        thread.start_new_thread(_auth, ())

    def _on_message(self, message_string):
        message = json.loads(message_string)
        if "message" in message and message["message"] == 'Stream Start':
            self.results[message['seqno']] = [message]
        elif message['seqno'] in self.results:
            self.results[message['seqno']].append(message)
        else:
            self.results[message['seqno']] = message

    def _on_error(self, error):
        # if connecting stop trying
        if self._connecting:
            logger.error("error: {} when connecting to {}"
                         .format(error, error.remote_ip))
            self._connecting = False
        raise Exception(error)

    def _on_close(self):
        pass

    @staticmethod
    def _build_command(command, *args, **kwargs):
        build_command = "{}".format(command)
        if args:
            build_command += " {}".format(' '.join(args))
        if kwargs:
            build_command += " {}".format(' '.join(
                ['--{} {}'.format(k, v) for k, v
                 in kwargs.items() if v is not None]))
            build_command += " {}".format(' '.join(
                ['--{}'.format(k, v) for k, v
                 in kwargs.items() if v is None]))
        return build_command

    def cmd(self, command, *args, **kwargs):
        def _get_session():
            if not self.dataset_id:
                raise Exception('Need a dataset_id to get a session')
            self.cmd('session', [self.dataset_id])

        if 'retry' in kwargs:
            retry = kwargs['retry']
            del kwargs['retry']
        else:
            retry = 0

        self.seqno += 1
        seqno = self.seqno
        final_command = self._build_command(command,
                                            *args,
                                            **kwargs)
        if retry > MAX_RETRIES:
            raise Exception('Could not run command {}'.format(final_command))

        logging.info(
            'sending sync command: {} {}'.format(seqno, final_command))
        try:
            self._ws.send("{} {}".format(seqno, final_command))
            # wait for result
            while self.seqno not in self.results:
                # if we loose conenction whiile waiting for result we exit
                if self._ws.sock is None:
                    logger.warn("we lost connection")
                    raise websocket.WebSocketConnectionClosedException()
                sleep(0.1)
            result = self.results[self.seqno]
        except websocket.WebSocketConnectionClosedException as e:
            logger.warn("Connection Closed")
            self.connect()
            kwargs['retry'] = retry + 1
            return self.cmd(command, *args, **kwargs)
        except Exception as e:
            logger.warn(e)
            kwargs['retry'] = retry + 1
            return self.cmd(command, *args, **kwargs)

        # if no session, init session first
        if 'message' in result and result['message'].startswith(
                'ERROR: Without a session') and self.dataset_id:
            _get_session()
            kwargs['retry'] = retry + 1
            return self.cmd(command, *args, **kwargs)
        logger.info("got results for seqno: {}".format(self.seqno))
        logger.info(result)
        if 'message' in result and 'ERROR:' in result['message']:
            raise LoreException(result['message'])
        return result

    def streaming_cmd(self, command, *args, **kwargs):
        """ return an iterator for streaming data"""
        self.seqno += 1
        seqno = self.seqno
        final_command = self._build_command(command, *args, **kwargs)
        self._ws.send("{} {}".format(seqno, final_command))
        while True:
            if self.seqno in self.results and len(
                    self.results[self.seqno]) != 0:
                # if we get an error right away
                if 'message' in self.results[self.seqno] and\
                        self.results[self.seqno]['message'].startswith(
                            'ERROR'):
                    raise LoreException(self.results[self.seqno]['message'])
                # otherwise we get an array
                # and grab the message in order one at the time
                result = self.results[self.seqno].pop(0)
                if result['message'] == 'Stream Start':
                    logger.info('stream starting')
                elif self.seqno == result['seqno'] and result[
                    'message'].startswith('ERROR'):
                    raise LoreException(result['message'])
                elif result['message'] == 'Stream Stop':
                    break
                elif self.seqno == result['seqno'] and result['message']:
                    yield result
                else:
                    raise Exception(result)

    def async_cmd(self, command, *args, **kwargs):
        self.seqno += 1
        seqno = self.seqno
        final_command = self._build_command(command, *args, **kwargs)
        logging.info(
            'sending async command: {} {}'.format(seqno, final_command))
        self._ws.send("{} {}".format(self.seqno, final_command))
        return seqno

    def get_result_for_cmd(self, seqno):
        if seqno not in self.results:
            return STATUS[1], {}
        else:
            result = self.results[self.seqno]
            if hasattr(result, 'message') and 'ERROR:' in result['message']:
                raise LoreException(result['message'])
            return STATUS[0], self.results[seqno]
