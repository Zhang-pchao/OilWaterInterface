To use the Voronoi Collective Variables (CVs) code, place the three .cpp files in /your_plumed_path/plumed/src/colvar and compile PLUMED. Follow [plumed-feedstock](https://github.com/Zhang-pchao/plumed-feedstock/tree/devel) to overlay the default version or use the [LOAD](https://www.plumed.org/doc-v2.8/user-doc/html/_l_o_a_d.html) command.

VoronoiC0.cpp: This file calculates the total ionic charge in water, such as during the autoionization of 2 H2O molecules, which produces 1 OH⁻ and 1 H₃O⁺, resulting in a charge change from 0 to +2.

VoronoiIM.cpp: This file is used to identify the oxygen index of the OH⁻ ion.

VoronoiIP.cpp: This file is used to identify the oxygen index of the H₃O⁺ ion.

Running DPMD with Voronoi CVs to identify the ionic oxygen index can be affected by the Grotthuss mechanism of proton transfer, causing fluctuations in the index. To use the traditional MSD calculation method, we need to create a fake trajectory using a Python script, input it into VMD, and then calculate the ionic diffusion coefficient based on the [reference](https://www.theoj.org/joss-papers/joss.01698/10.21105.joss.01698.pdf).
