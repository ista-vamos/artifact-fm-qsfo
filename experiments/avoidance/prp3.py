#!/usr/bin/env python3

from sys import path
from os.path import abspath, dirname

path.append(abspath(f"{dirname(__file__)}/.."))

from runner import create_parser, parse_cmd, run

if __name__ == "__main__":
    parser = create_parser()

    parser.add_argument(
        "--d_min",
        help="Parameter 'd_min' of the formula",
        action="store",
        type=float,
        default=0.5,
    )

    parser.add_argument(
        "--horizon",
        help="Consider this horizon while monitoring (0.1 for the original P3 formula)",
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

    # PRP 3
    prp = f"|(x(t) - ox_1(t))| > {args.d_min} \\and |(x(t) - ox_2(t))| > {args.d_min} \\and |(x(t) - ox_3(t))| > {args.d_min} \\and |(x(t) - ox_4(t))| > {args.d_min} \\and |(x(t) - ox_5(t))| > {args.d_min} \\and |(x(t) - ox_6(t))| > {args.d_min} \\and |(x(t) - ox_7(t))| > {args.d_min} \\and |(x(t) - ox_8(t))| > {args.d_min}"

    # do it!
    run(prp, args)
