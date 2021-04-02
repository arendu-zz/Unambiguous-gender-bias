#!/bin/bash
set -e
for ss in s xl xs; do
  echo $ss
  python gen.py ../grammars/$ss/grammar ../generated/$ss/source 
done
