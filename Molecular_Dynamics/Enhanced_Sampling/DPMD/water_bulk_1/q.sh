#!/bin/bash -l
#PBS -l select=1:ncpus=4:mpiprocs=4:ngpus=1
#PBS -l walltime=24:00:00  
#PBS -j oe
#PBS -N bul75
#PBS -q gpu_a100

cd $PBS_O_WORKDIR

# load dpmd
export PATH=/work/pzhang/app/miniconda/3/bin:$PATH
source activate deepmdkit_2.1.5_0202

# Run the application - the line below is just a random example.
lmp -i in.bulk > bulk.out
