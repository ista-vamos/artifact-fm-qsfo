#!/bin/bash

# MUST BE RUN FROM THE TOP DIR
DIR=$(readlink -f $(dirname $0))
TRACESDIR=$DIR/traces

echo "Starting $(date)"

OUTDIR=results/f16/prp123/
mkdir -p $OUTDIR

v_min=150  # 150mph ~ 240km/h
v_max=1500 # 1500mph ~ 2400km/h

T_rec=10
T_hold=10
HORIZON=20 # T_rec + T_hold

for TRACE in $TRACESDIR/*.csv; do
  echo "Running on $TRACE"

  uv run python -OO ./quant.py "(alt(t) \ge 1000 \and alt(t) \le 45000) \and (vt(t) \ge ${v_min} \and vt(t) \le ${v_max}) \and ((alt(t) >= 1640) \or (exists t_r \in [0, ${T_rec}]. forall t_h \in [0, ${T_hold}]: (alt(t + t_r + t_h) >= 2300)))" \
    $TRACE --samp 0.033 --horizon $HORIZON --csv $OUTDIR/$(basename ${TRACE}) --no-stdout || break

done

echo "Finished $(date)"
