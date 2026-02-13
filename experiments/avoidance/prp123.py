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
        "--T_max",
        help="Parameter 'T_max' of the formula",
        action="store",
        type=float,
        default=0.01,
    )

    parser.add_argument(
        "--ax_max",
        help="Parameter 'ax_max' of the formula (maximal velocity in the x direction)",
        action="store",
        type=float,
        default=0.01,
    )

    parser.add_argument(
        "--ay_max",
        help="Parameter 'ay_max' of the formula (maximal velocity in the y direction)",
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

    parser.add_argument(
        "--d_min",
        help="Parameter 'd_min' of the formula",
        action="store",
        type=float,
        default=0.5,
    )

    args = parse_cmd(parser)

    # PRP 1 + 2 + 3
    prp = f"(t < {args.t_s} \\or vx(t) < {args.v_max}) \\and (|(vx(t) - vx(t - 0.1))| < {args.ax_max} \\and |(vy(t) - vy(t - 0.1))| < {args.ay_max} \\and |(u3(t) - u3(t - 0.1))| < {args.T_max}) \\and (|(x(t) - ox_1(t))| > {args.d_min} \\and |(x(t) - ox_2(t))| > {args.d_min} \\and |(x(t) - ox_3(t))| > {args.d_min} \\and |(x(t) - ox_4(t))| > {args.d_min} \\and |(x(t) - ox_5(t))| > {args.d_min} \\and |(x(t) - ox_6(t))| > {args.d_min} \\and |(x(t) - ox_7(t))| > {args.d_min} \\and |(x(t) - ox_8(t))| > {args.d_min})"

    # do it!
    run(prp, args)
