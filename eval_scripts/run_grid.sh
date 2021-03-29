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
if [ $# -ne 3 ]; then
  echo 1>&2 "Usage: $0 src_file tgt_lang tgt_gen"
  exit 3
fi
src_file=$1
tgt=$2
tgt_gen=$3
echo 'rerun cmd:' sbatch run_grid.sh $1 $2 $3
cmd="python translate.py ${src_file}.en $tgt > ${src_file}.gen.$tgt"
echo 'cmd:' $cmd
eval $cmd
cmd="python tag.py ${src_file}.gen.$tgt $tgt"
echo 'cmd:' $cmd
eval $cmd
cmd="python align_and_score.py ${src_file}.en ${src_file}.gen.$tgt.tok ${src_file}.gen.$tgt.tag /checkpoint/adirendu/Unambiguous-gender-bias/grammars/occupation_list.txt  $tgt_gen > ${src_file}.gen.$tgt.scores"
echo 'cmd:' $cmd
eval $cmd
echo "done"
