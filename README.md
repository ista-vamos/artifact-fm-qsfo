# Artifact for *Monitoring quantified signal first-order logic

Software artifact for the paper *Monitoring quantified first-order logic*
accepted at FM 2026.

## Setup artifact

### Building the artifact

#### Building the docker image

```sh
docker build . -t qsfo
```

#### Building from sources

The project does not need any compilation, only installing dependencies.
By default, we use [uv] package manager. If you have [uv], simply run:

```
uv sync
```

Alternatively, `qsfo` may be build also with Poetry or using `pip` (see the list of
dependencies in `qsfo/pyproject.toml`).

## Running experiments

### Running the smoke-test

From the artifact directory, run

```sh
just smoketest
```

A smoke-test can take a few minutes.

### Running experiments

Run one of the following commands, depending on what experiments you want to run.

```sh
just run-short    # Run experiments with 10 random benchmarks in each category
just run-medium   # Run experiments on with random benchmarks in each category
just run-full     # Run full experiments
```

Short experiments should take a bit more then 1 hour, full experiments will take more than 24 hours.
To run single experiments (properties P1, P2, P3 or P 1+2+3 in avoidance or f16 simulator),
see `just --help`.

Results are stored as CSV files into the directory from which you run the experiments.
In case of using the docker image, this directory is `/opt/artifact/results` and
is mounted to the host system.
The results are automatically analyzed and table shown after the experiments finish.

### Other comments

- The source code of `qsfo` project (`qsfo/` directory) used in this paper differs
  slightly from the source code used for the original experiments: there have benchmarks
  comments structural and cosmetic changes, and added missing features to the parser.
  The monitoring algorithm itself stayed untouched. The original source code
  is attached in `qsfo-paper-src.zip`.
