#!/bin/bash

# MUST BE RUN FROM THE TOP DIR
# (just will take care of that)

# Parameters
vx_max=1
ignore_time=2

DIR=$(readlink -f "$(dirname "$0")")
TRACESDIR=$DIR/traces
QSFODIR=${DIR}/../../qsfo/

echo "Starting $(date)"
echo "  .. vx_max = ${vx_max}, ignore_time = ${ignore_time}"

OUTDIR=${DIR}/../results/avoidance/prp1_${vx_max}-${ignore_time}/
mkdir -p "$OUTDIR"

for TRACE in "${TRACESDIR}/"*.csv; do
  echo "Running on $TRACE"

  uv run python -OO "${QSFODIR}/main.py" "t < ${ignore_time} \or vx(t) < ${vx_max}" \
    "$TRACE" --samp 0.1 --horizon 0 --csv "$OUTDIR/$(basename "${TRACE}")" --no-stdout || break

done

echo "Finished $(date)"
