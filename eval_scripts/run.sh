#!/bin/bash
set -e
tgt=$1
#python translate.py ../data/mofc.en $tgt > mofc.gen.$tgt
#python tag.py mofc.gen.$tgt $tgt # uses GPU
python align_and_score.py ../data/mofc.en mofc.gen.$tgt.tok mofc.gen.$tgt.tag ../data/occ.en Fem #> mofc.gen.$tgt.scores
