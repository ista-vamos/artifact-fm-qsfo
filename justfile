# -------------------------------------------------
# Variables
# -------------------------------------------------

# Default recipe (runs when `just` is invoked with no args)
default:
    @just --list

smoketest:
  @just run-avoidance --n-random-traces=1
  @just run-f16 --n-random-traces=1 --timeout=20

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

run-f16-P1 *args:
  uv run experiments/f16/prp1.py \
    --traces experiments/f16/traces \
    --out results/f16/prp1 {{ args }}

run-f16-P2 *args:
  uv run experiments/f16/prp2.py \
    --traces experiments/f16/traces \
    --out results/f16/prp2  {{ args }}

run-f16-P3 *args:
  uv run experiments/f16/prp3.py \
    --traces experiments/f16/traces \
    --out results/f16/prp3  {{ args }}

run-f16-P123 *args:
  uv run experiments/f16/prp123.py \
    --traces experiments/f16/traces \
    --out results/f16/prp123  {{ args }}

run-f16 *args:
  @just run-f16-P1 {{args}}
  @just run-f16-P2 {{args}}
  @just run-f16-P3 {{args}}
  @just run-f16-P123 {{args}}

run-short:
  @just run-avoidance --n-random-traces=50 --timeout=30
  @just run-f16  --n-random-traces=10 --timeout=30

run-medium:
  @just run-avoidance --timeout=60
  @just run-f16 --n-random-traces=20 --timeout=60

run-full:
  @just run-avoidance
  @just run-f16

