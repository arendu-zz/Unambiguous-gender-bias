#!/bin/bash
set -e
#for ll in `cat all_langs.txt`; do
size=s
for ll in ar de es hi; do #`cat all_langs.txt`; do
  echo $ll
  for model in 'opus-mt' 'mbart50_m2m' 'm2m_100_418M' 'm2m_100_1.2B'; do 
    sbatch run_grid.sh $ll $model $size
  done
done
