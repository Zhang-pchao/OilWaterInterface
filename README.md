# Oil-Water Interface Study Resources

This repository gathers the inputs, scripts, models, and analysis utilities used in the study *“Propensity of water self-ions at air(oil)-water interfaces revealed by deep potential molecular dynamics with enhanced sampling.”* It is intended to help you reproduce the workflows that connect density functional theory (DFT), DeePKS, and DeePMD simulations, and to explore the collective variables (CVs) developed for enhanced sampling.

## Repository Layout

- **Analysis_Scripts/** – Post-processing utilities, including charge conversion scripts (`charge/`), format converters between *dpdata* and various electronic-structure codes (`dpdata/`), and tools to reconstruct 1D/2D free-energy surfaces (`fes/`).
- **DFT_Calculation/** – CP2K reference calculations, with ready-to-use `m062x` and `pbe` input decks plus submission scripts in `cp2k_input/`.
- **DeePKS_Iteration/** – DeePKS self-consistent iteration assets for the 2c10h22_44h2o system, covering iteration configuration (`iter/`), projector generation (`projector/`), and training datasets stored as NumPy archives under `systems/`.
- **DeePMD_Training/** – Frozen models, learning curves, run configurations, and submission helpers for both DP and DC networks (`DP/`, `DC/`). The top-level README highlights their use in the Langmuir publication.
- **Ion_Diffusion_Coefficient/** – Inputs to evaluate ionic mobility with and without Voronoi CVs, including fake-trajectory generators for mean-squared-displacement analysis (`get_fake_trj_for_msd/`) and example LAMMPS/PLUMED setups for hydronium (`h3o_dpmd/`) and hydroxide (`oh_dpmd/`).
- **Molecular_Dynamics/** – LAMMPS and PLUMED configurations for equilibrium (`No_Enhanced_Sampling/`) and enhanced-sampling (`Enhanced_Sampling/`) simulations, such as OPES runs for air–water and oil–water slabs, DPLRMD bulk setups, configuration sampling jobs, and CV derivative testing scripts.
- **Voronoi_CVs/** – Source code for the Voronoi-based collective variables used to track ionic indices, charges, distances, and slab locations, accompanied by a dedicated README.

## Tutorials

- [From DFT to DeePKS to DeePMD | DeePKS Basics](https://nb.bohrium.dp.tech/detail/8742877753)
- [From DFT to DeePKS to DeePMD | DeePKS Toturials](https://nb.bohrium.dp.tech/detail/7144731675)
- [OPES (on-the-fly probability enhanced sampling)](https://bohrium.dp.tech/notebooks/9874998164)
- [Voronoi CVs for enhanced sampling autoionization and tautomerism](https://bohrium.dp.tech/notebooks/83327491785)
- *Note:* The above web links have Chinese to English translations.

## Dataset and Model Availability

- The datasets for training and testing the [DP](https://github.com/Zhang-pchao/OilWaterInterface/tree/main/DeePMD_Training/DP) and [DC](https://github.com/Zhang-pchao/OilWaterInterface/tree/main/DeePMD_Training/DC) models are uploaded to [AIS Square](https://www.aissquare.com/datasets/detail?pageType=datasets&id=299) and [Zenodo](https://zenodo.org/records/14780363).
- The compressed DP model is uploaded to [AIS Square](https://www.aissquare.com/models/detail?pageType=models&id=298) and [Zenodo](https://zenodo.org/records/14780363).
- DC model training steps are available [here](https://github.com/Zhang-pchao/predict_atomic_charge).

## Packages Used

### 1. plumed_v2.8.1_patch
- Requires installation of the [OPES](https://www.plumed.org/doc-v2.8/user-doc/html/_o_p_e_s.html) module. To use additional Voronoi CVs code, put [.cpp files](https://github.com/Zhang-pchao/OilWaterInterface/tree/main/Voronoi_CVs) into `/your_plumed_path/plumed/src/colvar`, and then compile PLUMED, or use the [LOAD](https://www.plumed.org/doc-v2.8/user-doc/html/_l_o_a_d.html) command directly.
- More Voronoi CVs can be utilized for the [glycine tautomerism case](https://github.com/Zhang-pchao/GlycineTautomerism/tree/main).

### 2. deepmd-kit_v2.1.5
- **Re-compile PLUMED** – Incorporate LAMMPS and PLUMED by following the [plumed-feedstock](https://github.com/Zhang-pchao/plumed-feedstock/tree/devel) recipe to overlay the default PLUMED version.
- **No Re-compile (quick test)** – If you do **not** want to re-compile PLUMED, use the [LOAD](https://www.plumed.org/doc-v2.8/user-doc/html/_l_o_a_d.html) command at runtime.

### 3. deepks-kit_v0.1

### 4. abacus_v3.0.5

### 5. cp2k_v9.1
Incorporating PLUMED

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
