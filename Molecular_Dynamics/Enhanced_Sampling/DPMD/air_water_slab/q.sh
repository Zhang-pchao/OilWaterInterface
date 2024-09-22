module purge
#module load cuda/11.6
source activate deepmd-kit_v2.2.9_vcv

# Run the application - the line below is just a random example.
lmp -i in.oil > oil.out
