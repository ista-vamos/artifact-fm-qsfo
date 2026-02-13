#!/usr/bin/env python3

from sys import path
from os.path import abspath, dirname

path.append(abspath(f"{dirname(__file__)}/.."))

from runner import create_parser, parse_cmd, run

if __name__ == "__main__":
    parser = create_parser()

    parser.add_argument(
        "--horizon",
        help="Consider this horizon while monitoring (0 for the original P1 formula)",
        action="store",
        type=int,
        default=0,
    )

    parser.add_argument(
        "--sampling",
        help="Consider this sampling interval (0.033 for prerecorded traces)",
        action="store",
        type=float,
        default=0.033,
    )

    args = parse_cmd(parser)

    # PRP 1
    prp = "alt(t) \\ge 1000 \\and alt(t) \\le 45000"

    # do it!
    run(prp, args)
