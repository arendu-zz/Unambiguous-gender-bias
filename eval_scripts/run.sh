#!/bin/bash
set -e
tgt=de
python translate.py ../data/mofc.en $tgt > mofc.gen.$tgt
python tag.py mofc.gen.$tgt $tgt # uses GPU
python align_and_score.py ../data/mofc.en mofc.gen.$tgt.tok mofc.gen.$tgt.tag ../data/en-$tgt.dict Fem > mofc.gen.$tgt.scores
