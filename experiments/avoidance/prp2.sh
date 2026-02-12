#!/bin/bash

# MUST BE RUN FROM THE TOP DIR
DIR=$(readlink -f $(dirname $0))

OUTDIR=results/avoidance/prp2-01/
mkdir -p $OUTDIR

TRACESDIR=$DIR/traces

echo "Starting $(date)"

vx_max=0.01 # 0.1 * dx where dx = 0.1
vy_max=0.01 # 0.1 * dy where dy = 0.1
T_max=0.01  # 0.1 * dy where dy = 0.1

for TRACE in $TRACESDIR/*.csv; do
  echo "Running on $TRACE"

  echo "  .. vx_max = $vx_max, vy_max = $vy_max, T_max = $T_max"
  uv run python -OO ./quant.py "|(vx(t) - vx(t - 0.1))| < ${vx_max} \and |(vy(t) - vy(t - 0.1))| < ${vy_max} \and |(u3(t) - u3(t - 0.1))| < ${T_max}" \
    $TRACE --samp 0.1 --horizon 0.1 --csv $OUTDIR/$(basename ${TRACE}) --no-stdout || break

done

echo "Finished $(date)"
