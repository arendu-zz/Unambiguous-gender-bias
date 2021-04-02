#! /bin/bash
#################################################################################
#     File Name           :     test.sh
#     Description         :     Run this script with 'sbatch test.sh'
#################################################################################
#SBATCH --job-name=genderrun
#SBATCH --partition=learnfair
#SBATCH --nodes=1
#SBATCH --array=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=2048
#SBATCH --cpus-per-task=4
#SBATCH --signal=USR1
#SBATCH --open-mode=truncate
#SBATCH --time=72:00:00
#SBATCH --mail-user=adirendu@fb.com
#SBATCH --mail-type=fail


# Do your normal work here, e.g. run your training or eval executables. 
# They can be either in bash or other scripts invoked by srun.
set -e
module load anaconda3/5.0.1 cuda/10.1 cudnn/v7.6-cuda.10.0
source activate easyNMT
if [ $# -ne 3 ]; then
  echo 1>&2 "Usage: $0 tgt_lang model size"
  exit 3
fi
tgt=$1
model=$2
size=$3
proj=/checkpoint/adirendu/Unambiguous-gender-bias
echo 'rerun cmd:' sbatch run_grid.sh $tgt $model
src_file="$proj/generated/$size/source"
mkdir -p $proj/generated/$size/$model
tgt_file="$proj/generated/$size/$model/target"
if [[ -f "${tgt_file}.$tgt.tok.result" ]]; then
  for typ in "simple" "before_after" "context_A" "context_V" "context_AV" "context_npo_A" "generic"; do 
    cmd="python analyze_${typ}.py ${src_file}.ans ${src_file}.en ${src_file}.feats ${tgt_file}.$tgt.tok.result $proj/grammars/occupation_list.txt > ${tgt_file}.$tgt.tok.analysis.${typ}"
    echo $cmd
    eval $cmd
  done
  echo "done"
else
  echo "skip"
fi
