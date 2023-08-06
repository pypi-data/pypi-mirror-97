#!/usr/bin/env python3
"""Program's entry point."""
import sys
import time
from pathlib import Path

import humanize

from .argparse_wrapper import get_parsed_args
from .logs import get_logger


def main():
    """Program's main routine."""
    t_start = time.time()
    prog_name = Path(sys.argv[0]).name
    args = get_parsed_args(prog_name)
    logger = get_logger(prog_name, args.loglevel)
    if args.command is None:
        # Enforce this here instead of on the command's parser.add_subparsers
        # definition because add_subparsers only introduced the "required" arg
        # from python v3.7, and we want the code to work with python>=3.6.10.
        msg = "Cannot run {0} without a command! Please run "
        msg += "'{0} -h' for help."
        msg = msg.format(prog_name)
        logger.error(msg)
        sys.exit(1)
    args.func(args)
    elapsed = time.time() - t_start
    if elapsed >= 60:
        logger.debug(
            "Leaving 'main()'. Elapsed: %.2fs (~%s)",
            elapsed,
            humanize.precisedelta(elapsed),
        )
    else:
        logger.debug("Leaving 'main()'. Elapsed: %.2fs", elapsed)
