#!/bin/bash
set -e
for ll in `cat all_langs.txt`; do
  echo $ll
  sbatch run_grid.sh $ll
done
