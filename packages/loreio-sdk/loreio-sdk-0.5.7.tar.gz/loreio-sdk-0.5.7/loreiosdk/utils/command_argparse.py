"""
    Argument parsing classes for inner-program commands.
"""
import argparse
try:
    import copy_reg
except ImportError:
    import copyreg as copy_reg

__author__ = 'Bill Chickering'


class CommandArgumentError(Exception):
    pass


class CommandArgumentMessage(Exception):
    pass


class CommandArgumentStream(Exception):
    def __init__(self, generator):
        self.generator = generator


def make_action_class(func):
    """Returns a custom Action that executes the function `func`."""
    class ActionFunction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            self.nargs = 0
            func()
    return ActionFunction


def nargs_range(nmin, nmax):
    """Restricts nargs to be in range [`nmin`, `nmax`], inclusive."""
    class RequiredArgRangeAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if len(values) < nmin or len(values) > nmax:
                raise CommandArgumentError(
                    '{dest} requires between {nmin} and {nmax} args'.format(
                        dest=self.dest,
                        nmin=nmin,
                        nmax=nmax
                    )
                )
            setattr(args, self.dest, values)
    return RequiredArgRangeAction


class CommandArgumentParser(argparse.ArgumentParser):
    """
        Custom ArgumentParser that overrides printing and exiting
        behavior.
    """
    def __init__(self, **kwargs):
        """Record kwargs for pickling."""
        super(CommandArgumentParser, self).__init__(**kwargs)
        self.init_kwargs = kwargs

    def add_argument(self, *args, **kwargs):
        """Record args and kwargs for pickling."""
        super(CommandArgumentParser, self).add_argument(*args, **kwargs)
        if not hasattr(self, 'arg_params'):
            self.arg_params = []
        self.arg_params.append((args, kwargs))

    def print_usage(self, file=None):
        pass  # do nothing

    def print_help(self, file=None):
        raise CommandArgumentMessage(self.format_help())

    def error(self, message):
        raise CommandArgumentError(''.join([self.format_usage(), message]))


def cmd_arg_parser_unpickler(init_kwargs, arg_params):
    """Unpickling function for CommandArgumentParser objects."""
    parser = CommandArgumentParser(**init_kwargs)
    if arg_params is not None:
        for args, kwargs in arg_params:
            parser.add_argument(*args, **kwargs)
    return parser


def cmd_arg_parser_pickler(parser):
    """Pickling function for CommandArgumentParser objects."""
    return (
        cmd_arg_parser_unpickler,
        (
            parser.init_kwargs,
            parser.arg_params if hasattr(parser, 'arg_params') else None
        )
    )


copy_reg.pickle(CommandArgumentParser, cmd_arg_parser_pickler)
