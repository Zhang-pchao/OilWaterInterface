## Toturials
  - [From DFT to DeePKS to DeePMD | DeePKS Basics](https://nb.bohrium.dp.tech/detail/8742877753)
  - [From DFT to DeePKS to DeePMD | DeePKS Toturials](https://nb.bohrium.dp.tech/detail/7144731675)
  - [OPES (on-the-fly probability enhanced sampling)](https://bohrium.dp.tech/notebooks/9874998164)
  - [Voronoi CVs for enhanced sampling autoionization and tautomerism](https://bohrium.dp.tech/notebooks/83327491785)
  - Note: The above web links have Chinese to English translations.

## Dataset and model
  - The datasets for training and testing the [DP](https://github.com/Zhang-pchao/OilWaterInterface/tree/main/DeePMD_Training/DP) and [DC](https://github.com/Zhang-pchao/OilWaterInterface/tree/main/DeePMD_Training/DC) models are uploaded to [AIS Square](https://www.aissquare.com/datasets/detail?pageType=datasets&id=299) and [Zenodo](https://zenodo.org/records/14780363).
  - The compressed DP model is uploaded to [AIS Square](https://www.aissquare.com/models/detail?pageType=models&id=298) and [Zenodo](https://zenodo.org/records/14780363).
  - DC model training steps are available [here](https://github.com/Zhang-pchao/predict_atomic_charge).

## Packages Used

### 1. plumed_v2.8.1_patch
  - Requiring the installation of the [OPES](https://www.plumed.org/doc-v2.8/user-doc/html/_o_p_e_s.html) module. 
To use additional Voronoi CVs code, put [.cpp files](https://github.com/Zhang-pchao/OilWaterInterface/tree/main/Voronoi_CVs) into /your_plumed_path/plumed/src/colvar, and then compile plumed, or use the [LOAD](https://www.plumed.org/doc-v2.8/user-doc/html/_l_o_a_d.html) command directly.
  - More Voronoi CVs can be utilized for the [glycine tautomerism case](https://github.com/Zhang-pchao/GlycineTautomerism/tree/main).

### 2. deepmd-kit_v2.1.5
  - **Re-compile PLUMED**  
  Incorporate LAMMPS and PLUMED by following the [plumed-feedstock](https://github.com/Zhang-pchao/plumed-feedstock/tree/devel) recipe to overlay the default PLUMED version.

  - **No Re-compile (quick test)**  
  If you do **not** want to re-compile PLUMED, use the [LOAD](https://www.plumed.org/doc-v2.8/user-doc/html/_l_o_a_d.html) command at runtime and update the header paths in the relevant `.cpp` files (Prior to executing the job, it may be necessary to export the library path: `export LD_LIBRARY_PATH=/your_path/plumed_build-prefix/lib:$LD_LIBRARY_PATH`
):

    ```cpp
    #include "/your_path/plumed_build-prefix/include/plumed/tools/NeighborList.h"
    #include "/your_path/plumed_build-prefix/include/plumed/tools/Communicator.h"
    #include "/your_path/plumed_build-prefix/include/plumed/tools/OpenMP.h"
    #include "/your_path/plumed_build-prefix/include/plumed/colvar/Colvar.h"
    #include "/your_path/plumed_build-prefix/include/plumed/tools/Matrix.h"
    #include "/your_path/plumed_build-prefix/include/plumed/colvar/ActionRegister.h"
  
### 3. deepks-kit_v0.1

### 4. abacus_v3.0.5

### 5. cp2k_v9.1
Incorporating plumed

## Paper Title

Propensity of water self-ions at air(oil)-water interfaces revealed by deep potential molecular dynamics with enhanced sampling, [Langmuir](https://pubs.acs.org/doi/full/10.1021/acs.langmuir.4c05004). [arXiv](https://arxiv.org/abs/2404.07027)

```bibtex
@article{Zhang_Langmuir_2025_v41_p3675,
  title        = {{Propensity of Water Self--Ions at Air(Oil)--Water Interfaces Revealed by Deep Potential Molecular Dynamics with Enhanced Sampling}},
  author       = {Pengchao Zhang and Xuefei Xu},
  year         = 2025,
  journal      = {Langmuir},
  volume       = 41,
  number       = 5,
  pages        = {3675--3683},
  doi          = {10.1021/acs.langmuir.4c05004},
}
