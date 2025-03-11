## Steps to Train the Charge Model

1. **Calculate Hirshfeld Charges in CP2K**  
   Add the following keyword in your CP2K input file to enable Hirshfeld charge calculation:  
   [Hirshfeld keyword](https://github.com/Zhang-pchao/OilWaterInterface/blob/main/DFT_Calculation/cp2k_input/m062x/m062x.inp#L145)

2. **Build the Training Dataset**  
   Extract the charge data (`atom_dos.npy`) from the `cp2k.out.log` file using this script:  
   [sp_cp2k2dp_charge.py](https://github.com/Zhang-pchao/predict_atomic_charge/blob/main/cp2k_Hirshfeld/sp_cp2k2dp_charge.py)

3. **Train the Charge Model**  
   Train the model following the settings in:  
   [run.json](https://github.com/Zhang-pchao/predict_atomic_charge/blob/main/model/run.json)

4. **More Information**  
   - For additional details, refer to the [DOS model manual](https://docs.deepmodeling.com/projects/deepmd/en/master/model/train-fitting-dos.html), the [Bohrium Notebook](https://bohrium.dp.tech/notebooks/6641686247) and the [paper](https://doi.org/10.1021/acs.langmuir.4c05004).  
   - The charge model is a simplified case of the DOS model, where the charge model is one-dimensional.
