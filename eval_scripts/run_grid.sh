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
#SBATCH --gpus=1
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
if [ $# -ne 1 ]; then
  echo 1>&2 "Usage: $0 tgt_lang"
  exit 3
fi
tgt=$1
proj=/checkpoint/adirendu/Unambiguous-gender-bias
echo 'rerun cmd:' sbatch run_grid.sh $1 $2 $3
src_file="$proj/generated/xs/source"
tgt_file="$proj/generated/xs/target"
cmd="python translate.py ${src_file}.en $tgt > ${tgt_file}.$tgt"
echo 'cmd:' $cmd
eval $cmd
cmd="python tag.py ${tgt_file}.$tgt $tgt"
echo 'cmd:' $cmd
eval $cmd
cmd="python align.py ${src_file}.en ${src_file}.ans ${tgt_file}.$tgt.tok ${tgt_file}.$tgt.tag $proj/grammars/occupation_list.txt"
echo 'cmd:' $cmd
eval $cmd
cmd="python score.py $proj/grammars/occupation_list.txt ${src_file}.en ${src_file}.ans ${tgt_file}.$tgt.tok.result > ${tgt_file}.$tgt.tok.scores"
echo 'cmd:' $cmd
eval $cmd
echo "done"
