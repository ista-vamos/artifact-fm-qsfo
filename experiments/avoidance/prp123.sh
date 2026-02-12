#!/bin/bash

# MUST BE RUN FROM THE TOP DIR
DIR=$(readlink -f $(dirname $0))
TRACESDIR=$DIR/traces

echo "Starting $(date)"

OUTDIR=results/avoidance/prp123/
mkdir -p $OUTDIR

vx_max=1
ignore_time=2

ax_max=0.01 # 0.1 * dx where dx = 0.1
ay_max=0.01 # 0.1 * dy where dy = 0.1
T_max=0.01  # 0.1 * dy where dy = 0.1
d_min=0.5

for TRACE in $TRACESDIR/*.csv; do
  echo "Running on $TRACE"

  uv run python -OO ./quant.py "(t < ${ignore_time} \or vx(t) < ${vx_max}) \and (|(vx(t) - vx(t - 0.1))| < ${ax_max} \and |(vy(t) - vy(t - 0.1))| < ${ay_max} \and |(u3(t) - u3(t - 0.1))| < ${T_max}) \and (|(x(t) - ox_1(t))| > ${d_min} \and |(x(t) - ox_2(t))| > ${d_min} \and |(x(t) - ox_3(t))| > ${d_min} \and |(x(t) - ox_4(t))| > ${d_min} \and |(x(t) - ox_5(t))| > ${d_min} \and |(x(t) - ox_6(t))| > ${d_min} \and |(x(t) - ox_7(t))| > ${d_min} \and |(x(t) - ox_8(t))| > ${d_min})" \
    $TRACE --samp 0.1 --horizon 0.1 --csv $OUTDIR/$(basename ${TRACE}) --no-stdout || break

done

echo "Finished $(date)"
