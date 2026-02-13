#!/usr/bin/env python3

from sys import path
from os.path import abspath, dirname

path.append(abspath(f"{dirname(__file__)}/.."))

from runner import create_parser, parse_cmd, run

if __name__ == "__main__":
    parser = create_parser()

    parser.add_argument(
        "--T_rec",
        help="Parameter 'T_rec' of the formula",
        action="store",
        type=float,
        default=10.0,
    )

    parser.add_argument(
        "--T_hold",
        help="Parameter 'T_hold' of the formula",
        action="store",
        type=float,
        default=10.0,
    )

    parser.add_argument(
        "--horizon",
        help="Consider this horizon while monitoring (T_rec + T_hold)",
        action="store",
        type=int,
        default=20,
    )

    parser.add_argument(
        "--sampling",
        help="Consider this sampling interval (0.1 for prerecorded traces)",
        action="store",
        type=float,
        default=0.033,
    )

    args = parse_cmd(parser)

    # PRP 3
    prp = f"((alt(t) >= 1640) \\or (exists t_r \\in [0, {args.T_rec}]. forall t_h \\in [0, {args.T_hold}]: (alt(t + t_r + t_h) >= 2300)))"
    # do it!
    run(prp, args)
