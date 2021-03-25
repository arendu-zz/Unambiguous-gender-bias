#!/bin/bash
set -e
python translate.py ../data/mofc.en es > mofc.gen.es
python tag.py mofc.gen.es es
python align_and_score.py mofc.en mofc.gen.es.tok mofc.gen.es.tag ../data/en-es.dict Fem > scores.es
