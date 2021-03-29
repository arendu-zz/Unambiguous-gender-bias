#!/bin/bash
set -e
for ll in `cat all_langs.txt`; do
  echo $ll
  for occ in fo mo; do 
    for adj in fa fs ma ms; do 
      for ctx in mc fc; do 
        g=/checkpoint/adirendu/Unambiguous-gender-bias/grammars/s/template.$occ.$adj.$ctx.en
        if [[ -f "$g" ]]; then
          echo "$g exists."
          sbatch run_grid.sh /checkpoint/adirendu/Unambiguous-gender-bias/grammars/s/template.$occ.$adj.$ctx $ll Masc
        fi
      done
    done
  done
done
