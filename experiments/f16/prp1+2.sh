#!/bin/bash

# MUST BE RUN FROM THE TOP DIR
DIR=$(readlink -f $(dirname $0))
TRACESDIR=$DIR/traces

echo "Starting $(date)"

OUTDIR=results/f16/prp1+2/
mkdir -p $OUTDIR

v_min=150  # 150mph ~ 240km/h
v_max=1500 # 1500mph ~ 2400km/h

for TRACE in $TRACESDIR/*.csv; do
  echo "Running on $TRACE"

  uv run python -OO ./quant.py "(alt(t) \ge 1000 \and alt(t) \le 45000) \and (vt(t) >= ${v_min} \and vt(t) <= ${v_max})" \
    $TRACE --samp 0.033 --horizon 0 --csv $OUTDIR/$(basename ${TRACE}) --no-stdout || break

done

echo "Finished $(date)"
