# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2017-2019 Jani Nikula <jani@nikula.org>

"""
Late, another terrible excuse.

An RFC5545 iCalendar search and manipulation tool.
"""

import argparse
import configparser
import inspect
import logging
import os
import sys
import textwrap

from late.command import log
from late import command
from late import __version__

def main():
    helpformatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog=command.late,
                                     description=__doc__.strip(),
                                     formatter_class=helpformatter,
                                     add_help=False, allow_abbrev=False)
    parser.add_argument('--config', default='~/.laterc',
                        help='Configuration file.')
    parser.add_argument('--profile', default='DEFAULT',
                        help='Configuration profile.')
    parser.add_argument('--input', dest='source', action='append', default=[],
                        help='Input files or directories.')
    parser.add_argument('--verbose', action='count', default=0,
                        help='Increase verbosity.')
    parser.add_argument('--quiet', action='count', default=0,
                        help='Decrease verbosity.')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__),
                        help='Show version number and exit.')
    parser.add_argument('--help', action='help',
                        help='Show this help message and exit.')

    subparsers = parser.add_subparsers(title='commands',
                                       metavar='COMMAND',
                                       description="For help on a particular "
                                       "command, run: '%(prog)s COMMAND --help'")

    for cmd, func in command.list_commands():
        doc = textwrap.dedent(func.__doc__).strip().replace('%', '%%')
        subparser = subparsers.add_parser(cmd,
                                          add_help=False,
                                          help=doc.splitlines()[0],
                                          description=doc,
                                          formatter_class=helpformatter)
        subparser.set_defaults(func=func)
        subparser.add_argument('--help', action='help',
                               help='Show this help message and exit.')

        # add command specific options
        if (cmd == 'explain' or cmd == 'search' or cmd == 'pretty' or
            cmd == 'dump'):
            subparser.add_argument('query', metavar='SEARCH-TERM',
                                   nargs='*', default=[])
        if cmd == 'search':
            subparser.add_argument('--output',
                                   choices=command.printers,
                                   default='uid')
        elif cmd == 'pretty':
            subparser.add_argument('--output',
                                   choices=command.printers,
                                   default='pretty')


    args = parser.parse_args()

    log.setLevel(log.getEffectiveLevel() + 10 * args.quiet - 10 * args.verbose)

    if not getattr(args, 'func', None):
        parser.print_usage()
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(os.path.expanduser(args.config))

    if len(args.source) == 0:
        ics = os.path.expanduser(config.get(args.profile, 'storage',
                                            fallback='~/.late.ics'))
        args.source = [ics]

    (arg_names, varargs, varkw) = inspect.getargs(args.func.__code__)
    kwargs = {key: getattr(args, key) for key in arg_names if key in args}

    try:
        args.func(**kwargs)
    except Exception as e:
        if log.isEnabledFor(logging.DEBUG):
            raise
        log.error(str(e))
        sys.exit(1)

main()
