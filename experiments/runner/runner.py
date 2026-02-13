#!/usr/bin/env python3
from random import randrange

import datetime
from subprocess import Popen, PIPE, TimeoutExpired
from os.path import basename, join, abspath, isdir
from os import listdir, makedirs, getcwd, getpgid, setsid, killpg
from sys import stderr, stdout
from multiprocessing import Pool
import signal

import argparse

# SELFDIR = join(dirname(__file__))
DIR = getcwd()
LOGFILE = join(DIR, "log.txt")


def errlog(*args):
    with open(LOGFILE, "w") as logf:
        for a in args:
            print(a, file=logf)


def run_monitor(arg):
    trace, prp, args = arg
    cmd = args.qsfo_cmd.split()
    cmd.append(prp)
    cmd.append(trace)
    cmd.append(f"--samp={args.sampling}")
    cmd.append(f"--horizon={args.horizon}")
    cmd.append(f"--csv={args.out}/{basename(trace)}")
    cmd.append("--no-stdout")

    p = Popen(cmd, stderr=PIPE, stdout=PIPE, preexec_fn=setsid)
    try:
        out, err = p.communicate(timeout=args.timeout)
        if p.returncode != 0:
            errlog("------", " ".join(cmd), "------", out, "------", err)
    except TimeoutExpired:
        killpg(getpgid(p.pid), signal.SIGTERM)
        out, err = p.communicate(timeout=10)
    return (trace, p.returncode, cmd, out, err)


def get_params(traces_dir, traces, prp, args):
    # yield trace, prp, args
    for t in traces:
        yield abspath(join(traces_dir, t)), prp, args


def run(prp, args):
    print(f"\nMonitoring \033[0;32m{prp}\033[0m\n")
    print(f" ... running using {args.j or 'automatic # of'} processes")
    if args.j is None:
        print(" ... (the number of used processes can be adjusted by parameter `-j`)")

    print(f" ... it's {datetime.datetime.now().time()}")
    stdout.flush()

    print(f" ... finding CSV traces in `{args.traces}`")
    traces_list = [fl for fl in listdir(args.traces) if fl.endswith(".csv")]
    n_traces = len(traces_list)
    print(f" ... found {n_traces} traces")

    if n_traces == 0:
        raise RuntimeError(f"Found no traces in `{args.traces}`")

    n_random_traces: None | int = args.n_random_traces
    if n_random_traces is not None and n_random_traces < n_traces:
        print(f" ... randomly selecting {n_random_traces} traces")
        selected_traces = [
            traces_list[randrange(0, n_traces)] for _ in range(n_random_traces)
        ]
    else:
        selected_traces = traces_list

    verbose = args.verbose

    N = len(selected_traces)
    n = 0

    print(" ... altogether,", N, "runs get executed")
    print("-------------------------------------")

    if isdir(args.out):
        print(
            f"Storing outputs to directory `{args.out}` (overwriting files that might be there)"
        )
        print("-------------------------------------")
    else:
        print(f" ... creating directory `{args.out}`")
        makedirs(args.out, exist_ok=True)
        print("-------------------------------------")

    with Pool(processes=args.j) as pool:
        for result in pool.imap_unordered(
            run_monitor, get_params(args.traces, selected_traces, prp, args)
        ):
            trace, exitcode, cmd, out, err = result
            if exitcode != 0:
                print(f"Failed running monitor, see `{LOGFILE}`", file=stderr)

            progress = 100 * (n / N)
            if verbose:
                print(f"{progress: .2f}%: finished", trace)
            else:
                print(f"\r\033[32;1mDone: {progress: .2f}%\033[0m", end="")

            n += 1

        print("\nAll done!")
        print(f" ... it's {datetime.datetime.now().time()}")
        print("-------------------------------------")
        print(f"Results stored into `{args.out}`")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", metavar="PROC_NUM", action="store", type=int)
    parser.add_argument(
        "--out",
        help="Name of the output file. Default is 'out.csv'",
        action="store",
        default=join(DIR, "results"),
    )
    parser.add_argument(
        "--verbose",
        help="Print some extra messages",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--traces", help="Directory with traces", action="store", required=True
    )

    parser.add_argument(
        "--timeout",
        help="Timeout in seconds (default is no timeout)",
        action="store",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--n-random-traces",
        help="Select a subset of `n` random traces from the given traces",
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

    return parser


def parse_cmd(parser):
    args = parser.parse_args()
    args.out = abspath(args.out)

    return args
