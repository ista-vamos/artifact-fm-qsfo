#!/usr/bin/env python3
from random import randrange

import datetime
from subprocess import Popen, PIPE, TimeoutExpired
from os.path import dirname, basename, join, isfile, isdir
import os
from os import listdir, access, X_OK
from sys import stderr, stdout
from multiprocessing import Pool
import signal

import argparse


def errlog(*args):
    with open(join(dirname(__file__), "log.txt"), "a") as logf:
        for a in args:
            print(a, file=logf)


def run_monitor(trace, prp, args):
    cmd = args.qsfo_cmd.split("")
    cmd.append(prp)
    cmd.append(trace)
    cmd.append(f"--samp={args.sampling}")
    cmd.append(f"--horizon={args.horizon}")
    cmd.append(f'--csv="{args.out}/{basename(trace)}')
    cmd.append("--no-stdout")

    p = Popen(cmd, stderr=PIPE, stdout=PIPE, preexec_fn=os.setsid)
    try:
        out, err = p.communicate(timeout=args.timeout)
        if p.returncode != 0:
            errlog(p, out, err)
    except TimeoutExpired:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        out, err = p.communicate(timeout=10)
    return (trace, p.returncode, out, err)


def get_params(traces, prp, args):
    # yield trace, prp, args
    for t in traces:
        yield t, prp, args


def run(args):
    print(
        f"\033[1;34m[{datetime.datetime.now().time()}] Running using {args.j or 'automatic # of'} workers\n\033[0m",
    )
    stdout.flush()

    print(f" ... finding CSV traces in `{args.traces}`")
    traces_list = [fl for fl in listdir(args.traces) if fl.endswith(".csv")]
    n_traces = len(traces_list)
    print(f" ... found {n_traces} traces")

    n_random_traces: None | int = args.n_random_traces
    if n_random_traces is not None:
        print(f" ... randomly selecting {n_random_traces} traces")
        selected_traces = [
            traces_list[randrange(0, n_traces)] for _ in range(n_random_traces)
        ]
    else:
        selected_traces = traces_list

    # PRP 1
    prp = f"t < {args.ignore_time} \or vx(t) < {args.vx_max}"

    verbose = args.verbose

    N = len(selected_traces)
    n = 0

    print("Altogether,", N, "runs get executed\n")
    print("-------------------------------------")

    if isdir(args.out):
        print("Storing outputs to directory (overwriting files that might be there)")
        print("-------------------------------------")

    with Pool(processes=args.j) as pool, open(args.out, "w") as out:
        for result in pool.imap_unordered(
            run_monitor, get_params(selected_traces, prp, args)
        ):
            trace, exitcode, out, err = result
            if exitcode != 0:
                errlog("Failed running monitor:")
                errlog(out)
                errlog(err)

            progress = 100 * (n / N)
            if verbose:
                print(f"{progress: .2f}%: finished", trace)
            else:
                print(f"\r\033[32;1mDone: {progress: .2f}%\033[0m", end="")

            n += 1

        print("\nAll done!")
        print("Results stored into", args.out)


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", metavar="PROC_NUM", action="store", type=int)
    parser.add_argument(
        "--out",
        help="Name of the output file. Default is 'out.csv'",
        action="store",
        default="out.csv",
    )
    parser.add_argument(
        "--verbose",
        help="Print some extra messages",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--traces",
        help="Directory with traces",
        action="store",
    )
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
    parser.add_argument(
        "--trials",
        help="How many times repeat each run",
        action="store",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--timeout",
        help="Timeout in seconds (default is no timeout)",
        action="store",
        type=int,
        default=None,
    )

    parser.add_argument(
        "--qsfo-cmd",
        help="How to run `qsfo`",
        action="store",
        default="python -OO qsfo/main.py",
    )

    args = parser.parse_args()

    if isinstance(args.traces_lens, str):
        args.traces_lens = list(map(int, args.traces_lens.split(",")))
    if isinstance(args.traces_nums, str):
        args.traces_nums = list(map(int, args.traces_nums.split(",")))
    if isinstance(args.bits, str):
        args.bits = list(map(int, args.bits.split(",")))

    args.monitors = args.monitors.split(",")

    return args


def shl_monitors(args):
    for m in args.monitors:
        if m.startswith("shl"):
            yield m


if __name__ == "__main__":
    args = parse_cmd()

    problem = False
    for mon in shl_monitors(args):
        mon = join(f"{hnl_dir}/{mon}", "monitor")
        if not (isfile(mon) and access(mon, X_OK)):
            print(
                f"Did not find sHL monitor ({mon}). Please run `'./generate-shl.sh` "
                "first (you may need to modify the script to generate the right monitor).",
                file=stderr,
            )
            problem = True

    for bits in args.bits:
        mon = join(f"{hnl_dir}/ehl-{bits}b", "monitor")
        if not (isfile(mon) and access(mon, X_OK)):
            print(
                f"Did not find eHL monitor for {bits} bits. Please run `'./generate-ehl.sh "
                f"{bits}b'` first.",
                file=stderr,
            )
            problem = True

    if problem:
        exit(1)

    # do it!
    run(args)
