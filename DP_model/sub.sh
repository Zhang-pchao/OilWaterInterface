#!/bin/bash
#PBS -l select=1:ncpus=4:mpiprocs=1:ngpus=1:ompthreads=4
#PBS -l walltime=23:50:00
#PBS -q gpu
#PBS -o dptrain.out
#PBS -j oe
#PBS -N oil100

# change dir submission dir
cd $PBS_O_WORKDIR

# source env
#source /projects/atomisticsimulations/Manyi/Miniconda3-DeepMD-2.1.0.env
# load dpmd
export PATH=/work/pzhang/app/miniconda/3/bin:$PATH
source activate deepmdkit_2.1.5

# run
if [ ! -f tag_0_finished ] ;then
    { if [ ! -f model.ckpt.index ]; then
        CUDA_VISIBLE_DEVICES=0 horovodrun -np 1
        dp train --mpi-log=master run.json ;
    else
        CUDA_VISIBLE_DEVICES=0 horovodrun -np 1
        dp train --mpi-log=master run.json --restart model.ckpt; fi }
    1>> train.log 2>> train.log
    { if test $? -ne 0; then touch tag_0_failure; 
	else
	  dp freeze && dp compress && touch tag_0_finished; fi }
fi

# Run the application - the line below is just a random examp
#dp train run.json
#dp train run.json --restart model.ckpt
#dp freeze
#dp compress
