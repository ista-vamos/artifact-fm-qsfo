# Artifact for *Quantitative Monitoring of Signal First-Order Logic

Software artifact for the paper *Quantitative Monitoring of Signal First-Order Logic*
accepted at FM 2026.

## Using artifact

We assume that you have loaded the docker image and entered the container, i.e.,
you have run something like:

```sh
docker load < qsfo-fm.tar.gz
docker run -ti -v "$(pwd)/results":/opt/artifact/results qsfo-fm
```

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
just run-short    # Run experiments that should finish in around 20 min
just run-medium   # Run experiments that should take around 80 min
just run-long     # Run experiments that should take several hours
just run-full     # Run full experiments (might be two days on single core)
```

To run single experiments (properties P1, P2, P3 or P 1+2+3 in avoidance or f16 simulator),
see `just --help`. For single experiments, you can also specify `-j N` to execute on `N`
cores. E.g., `just run-avoidance -j 4`. To use more cores in one of pre-defined configurations,
modify the `justfile`.

Results are stored as CSV files into the directory from which you run the experiments.
In case of using the docker image, this directory is `/opt/artifact/results` and
is mounted to the host system (the `-v` parameter of `docker run`).
The results are automatically analyzed and table shown after the experiments finish.
You can manually show the results by running `just results`.

### Structure of the artifact

```
\
  - experiments       -- scripts to run experiments + traces
  - qsfo              -- source code of monitors
  - justfile          -- configuration for `just`
  - pyproject.toml    -- configuration to install dependencies
  - stats.py          -- script to generate tables
```

The source code of `qsfo` project (the `qsfo/` directory) used in this artifact differs
slightly from the source code used for the original experiments: there have been small
structural and cosmetic changes, and added missing features to the parser.
The monitoring algorithm itself stayed untouched. The original source code
is attached in `qsfo-paper-src.zip`. You can also check out the newest code
at <https://github.com/ista-vamos/qsfo>.

### Using and modifying qsfo

To run the monitoring algorithm on a given CSV file, run:

```sh
uv run qsfo/main.py <formula> <csv-file>
```

Formulas assume a single free time variable `t`, other variables must be bound by
`exists` or `forall`. Logical operators can be written in as `&&` or `||`
or also as `\and` and `\or`. Note that these operators are binary,
so you have to write e.g. `(f(t) > 3 \and f(t) < 5) \and (f(t) \ge g(t)`
instead of `f(t) > 3 \and f(t) < 5 \and (f(t) \ge g(t)`.
For more about formula syntax, see the README in Github.

The main algorithm is implemented in `qsfo/monitoring/quantitative.py`.
The name of methods should mostly correspond to the names in the paper.

## Building the artifact

These steps are not necessary if you have loaded the docker image.

### Building the docker image

```sh
docker build . -t qsfo-fm
```

### Building from sources

The project does not need any compilation, only installing dependencies.
By default, we use [uv] package manager. If you have [uv], simply run:

```
uv sync
```

Alternatively, `qsfo` may be build also with Poetry or using `pip` (see the list of
dependencies in `qsfo/pyproject.toml`).
