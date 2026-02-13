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

    # v_min=150  # 150mph ~ 240km/h
    parser.add_argument(
        "--v_min",
        help="Parameter 'v_min' of the formula",
        action="store",
        type=float,
        default=150,
    )

    # v_max=1500 # 1500mph ~ 2400km/h
    parser.add_argument(
        "--v_max",
        help="Parameter 'v_max' of the formula",
        action="store",
        type=float,
        default=1500,
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

    # PRP 1 + 2 + 3
    prp = f"(alt(t) \\ge 1000 \\and alt(t) \\le 45000) \\and (((vt(t) \\ge {args.v_min}) \\and vt(t) \\le {args.v_max}) \\and ((alt(t) >= 1640) \\or (exists t_r \\in [0, {args.T_rec}]. forall t_h \\in [0, {args.T_hold}]: (alt(t + t_r + t_h) >= 2300))))"

    # do it!
    run(prp, args)
