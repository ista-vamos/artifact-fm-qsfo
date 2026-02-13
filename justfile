# -------------------------------------------------
# Variables
# -------------------------------------------------

# Default recipe (runs when `just` is invoked with no args)
default:
    @just --list

smoketest:
  @just run-avoidance  --n-random-traces=1

run-avoidance-P1 *args:
  uv run experiments/avoidance/prp1.py \
    --traces experiments/avoidance/traces \
    --out results/avoidance/prp1 {{ args }}

run-avoidance-P2 *args:
  uv run experiments/avoidance/prp2.py \
    --traces experiments/avoidance/traces \
    --out results/avoidance/prp2  {{ args }}

run-avoidance-P3 *args:
  uv run experiments/avoidance/prp3.py \
    --traces experiments/avoidance/traces \
    --out results/avoidance/prp3  {{ args }}

run-avoidance-P123 *args:
  uv run experiments/avoidance/prp123.py \
    --traces experiments/avoidance/traces \
    --out results/avoidance/prp123  {{ args }}

run-avoidance *args:
  @just run-avoidance-P1 {{args}}
  @just run-avoidance-P2 {{args}}
  @just run-avoidance-P3 {{args}}
  @just run-avoidance-P123 {{args}}

run:
  @just run-avoidance
  @just run-f16

# Build the project with all its features
# build-all:
#     {{ CARGO }} build --all-targets --all-features {{ profile_flag }}
#     @just build-python

