# -*- coding: utf-8 -*-
#
# Main entrypoint for package.
#
# ------------------------------------


# imports
# -------
import os
import sys
import types
import inspect
import argparse
from functools import partial

from . import __version__
from . import *


# parser
# ------
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=__version__)
subparsers = parser.add_subparsers()


# subcommands
# -----------
def run(args, func=len):
    """
    Run arbitrary method based on signature.
    """
    kwargs = {}

    # get arg set
    for key, val in vars(args).items():
        if not callable(val):
            kwargs[key] = val

    # run and print result
    sys.stdout.write(str(func(**kwargs)))
    sys.stdout.flush()
    return


for name in dir():
    if name[0] != '_' and name not in ['run', 'version', 'main']:
        command = eval(name)
        if isinstance(command, types.FunctionType):
            desc = inspect.getdoc(command).split('\n')
            desc = desc[0] if len(desc) else ''
            sub = subparsers.add_parser(name, description=desc)

            # inspect function to create args
            spec = inspect.signature(command)
            for name, param in spec.parameters.items():

                # positional argument
                if param.default == inspect._empty:
                    sub.add_argument(param.name)

                # optional argument
                else:
                    sub.add_argument('--' + param.name, default=param.default)

            # create the subparser
            subrun = partial(run, func=command)
            sub.set_defaults(func=subrun)


# exec
# ----
def main(argv=sys.argv[1:]):

    # handle piped input
    if len(argv) and argv[-1] == '-':
        data = sys.stdin.read()
        data = data.replace('\n', '')
        argv[-1] = data
        main(argv)
        return

    # parse
    args = parser.parse_args(argv)

    # handle empty subcommands
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    # go!
    args.func(args)
    return



if __name__ == "__main__":
    main()
