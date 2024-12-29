# Voronoi Collective Variables (CVs) for Ion Systems

This repository contains a set of Collective Variables (CVs) for simulating ion behavior in various systems using PLUMED. These CVs are particularly useful for studying the ionization of water molecules, ion distances, and ion localization in a slab system.

## Installation

To use the Voronoi Collective Variables (CVs) code:

1. Place the provided `.cpp` files in the following directory:  
   `/your_plumed_path/plumed/src/colvar`
   
2. Compile PLUMED. You can follow the [plumed-feedstock](https://github.com/Zhang-pchao/plumed-feedstock/tree/devel) to overlay the default version or use the `LOAD` command from the [PLUMED documentation](https://www.plumed.org/doc-v2.8/user-doc/html/_l_o_a_d.html).

## CV Directories and Their Functions

### 1. `CV_for_ion_charge`
These CVs calculate the ionic charges in water systems, such as during the autoionization of water molecules.

- **`VoronoiC0.cpp`**  
   Calculates the total ionic charge in water. For example, during the autoionization of two H₂O molecules, which produces OH⁻ and H₃O⁺, the charge changes from 0 to +2.

- **`VoronoiC1M.cpp`**  
   Calculates the total negative ionic charge of OH⁻.

- **`VoronoiC1P.cpp`**  
   Calculates the total positive ionic charge of H₃O⁺.

### 2. `CV_for_ion_distance`

- **`VoronoiD1.cpp`**  
   Calculates the ionic distance between one OH⁻ ion and one H₃O⁺ ion.

### 3. `CV_for_ion_index`
These CVs are used to identify the indices of ions in the system.

- **`VoronoiIM.cpp`**  
   Identifies the oxygen index of the OH⁻ ion.

- **`VoronoiIP.cpp`**  
   Identifies the oxygen index of the H₃O⁺ ion.

### 4. `CV_for_ion_location_in_slab`
These CVs are used to identify the absolute location of ions in a slab system, relative to a reference layer.

- **`VoronoiIMZ.cpp`**  
   Identifies the absolute location of the OH⁻ ion along the z-axis relative to the reference layer in a slab system.  
   - [Example](https://github.com/Zhang-pchao/OilWaterInterface/blob/main/Molecular_Dynamics/Enhanced_Sampling/DPMD/air_water_slab/input.plumed): Set `ZIDX=2` to calculate the z-axis location.  
   - Set `ZMID=53` to define the reference layer at 53 Ångströms along the z-axis.

- **`VoronoiIPZ.cpp`**  
   Identifies the absolute location of the H₃O⁺ ion along the z-axis relative to the reference layer in a slab system.
