module purge
#module load cuda/11.6
source activate /u/huyang/conda-envs/deepmd-kit_v2.2.9_vcv

# Run the application - the line below is just a random example.
lmp -i in.lmp > lmp.out
