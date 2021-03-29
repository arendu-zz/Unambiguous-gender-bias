#!/bin/bash
set -e
if [ $# -ne 3 ]; then
  echo 1>&2 "Usage: $0 src_file tgt_lang tgt_gen"
  exit 3
fi
echo $1 $2
src_file=$1
tgt=$2
tgt_gen=$3
python translate.py ${src_file}.en $tgt > ${src_file}.gen.$tgt
python tag.py ${src_file}.gen.$tgt $tgt # uses GPU
python align_and_score.py ${src_file}.en ${src_file}.gen.$tgt.tok ${src_file}.gen.$tgt.tag ../data/occ.en $tgt_gen > ${src_file}.gen.$tgt.scores
