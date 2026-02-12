#!/bin/bash

# MUST BE RUN FROM THE TOP DIR
DIR=$(readlink -f $(dirname $0))
TRACESDIR=$DIR/traces

echo "Starting $(date)"

OUTDIR=results/avoidance/prp1-1-2/
mkdir -p $OUTDIR

vx_max=1
ignore_time=2
echo "  .. vx_max = 1, ignore_time = 2"

for TRACE in $TRACESDIR/*.csv; do
  echo "Running on $TRACE"

  uv run python -OO ./quant.py "t < ${ignore_time} \or vx(t) < ${vx_max}" \
    $TRACE --samp 0.1 --horizon 0 --csv $OUTDIR/$(basename ${TRACE}) --no-stdout || break

done

echo "Finished $(date)"
