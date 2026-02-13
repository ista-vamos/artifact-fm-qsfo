#!/usr/bin/env python3

from sys import path
from os.path import abspath, dirname

path.append(abspath(f"{dirname(__file__)}/.."))

from runner import create_parser, parse_cmd, run

if __name__ == "__main__":
    parser = create_parser()

    parser.add_argument(
        "--T_max",
        help="Parameter 'T_max' of the formula",
        action="store",
        type=float,
        default=0.01,
    )

    parser.add_argument(
        "--vx_max",
        help="Parameter 'vx_max' of the formula (maximal velocity in the x direction)",
        action="store",
        type=float,
        default=0.01,
    )

    parser.add_argument(
        "--vy_max",
        help="Parameter 'vy_max' of the formula (maximal velocity in the y direction)",
        action="store",
        type=float,
        default=0.01,
    )

    parser.add_argument(
        "--horizon",
        help="Consider this horizon while monitoring (0.1 for the original P2 formula)",
        action="store",
        type=int,
        default=0.1,
    )

    parser.add_argument(
        "--sampling",
        help="Consider this sampling interval (0.1 for prerecorded traces)",
        action="store",
        type=float,
        default=0.1,
    )

    args = parse_cmd(parser)

    # PRP 2
    prp = f"|(vx(t) - vx(t - 0.1))| < {args.vx_max} \\and |(vy(t) - vy(t - 0.1))| < {args.vy_max} \\and |(u3(t) - u3(t - 0.1))| < {args.T_max}"

    # do it!
    run(prp, args)
