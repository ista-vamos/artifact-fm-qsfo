#!/bin/bash

# MUST BE RUN FROM THE TOP DIR
DIR=$(readlink -f $(dirname $0))

OUTDIR=results/avoidance/prp3-05/
mkdir -p $OUTDIR

TRACESDIR=$DIR/traces

echo "Starting $(date)"

d_min=0.5

for TRACE in $TRACESDIR/*.csv; do
  echo "Running on $TRACE"

  uv run python -OO ./quant.py "|(x(t) - ox_1(t))| > ${d_min} \and |(x(t) - ox_2(t))| > ${d_min} \and |(x(t) - ox_3(t))| > ${d_min} \and |(x(t) - ox_4(t))| > ${d_min} \and |(x(t) - ox_5(t))| > ${d_min} \and |(x(t) - ox_6(t))| > ${d_min} \and |(x(t) - ox_7(t))| > ${d_min} \and |(x(t) - ox_8(t))| > ${d_min}" \
    $TRACE --samp 0.1 --horizon 0 --csv $OUTDIR/$(basename ${TRACE}) --no-stdout || break
  break

done

echo "Finished $(date)"
