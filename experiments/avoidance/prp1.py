#!/usr/bin/env python3

from sys import path
from os.path import abspath, dirname

path.append(abspath(f"{dirname(__file__)}/.."))

from runner import create_parser, parse_cmd, run

if __name__ == "__main__":
    parser = create_parser()

    parser.add_argument(
        "--t_s",
        help="Parameter 't_s' of the formula (after this time, the velocity must be less than v_max)",
        action="store",
        type=float,
        default=2.0,
    )

    parser.add_argument(
        "--v_max",
        help="Parameter 'v_max' of the formula (maximal velocity in the x direction)",
        action="store",
        type=float,
        default=1.0,
    )

    parser.add_argument(
        "--horizon",
        help="Consider this horizon while monitoring (0 for the original P1 formula)",
        action="store",
        type=int,
        default=0,
    )

    parser.add_argument(
        "--sampling",
        help="Consider this sampling interval (0.1 for prerecorded traces)",
        action="store",
        type=float,
        default=0.1,
    )

    args = parse_cmd(parser)

    # PRP 1
    prp = f"t < {args.t_s} \\or vx(t) < {args.v_max}"

    # do it!
    run(prp, args)
