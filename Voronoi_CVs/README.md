# Voronoi collective variables for water autoionization and interfaces

This directory contains the PLUMED C++ collective variables used to detect water self-ions, measure OH⁻/H₃O⁺ separation, identify the ion carrier, and locate the carrier relative to a slab reference plane.

These files are **paper-specific legacy Actions**. For a general implementation with explicit `CENTERS`, `ASSIGNED`, `REFERENCE`, physical axes, analytical derivatives, and a documented exact-versus-neighbor-list workflow, see the [Reactive Soft-Voronoi collective-variable guide](https://zhang-pchao.github.io/code/reactive-voronoi).

## Inventory

| Directory | Source | Registered Action | Output and intended use |
| --- | --- | --- | --- |
| `CV_for_ion_charge` | `VoronoiC0.cpp` | `VORONOIC0` | Sum of squared water-site coordination defects; nonnegative ion-activity diagnostic. |
| `CV_for_ion_charge` | `VoronoiC1M.cpp` | `VORONOIC1M` | Sum of negative water-site defects; OH⁻ activity branch. |
| `CV_for_ion_charge` | `VoronoiC1P.cpp` | `VORONOIC1P` | Sum of positive water-site defects; H₃O⁺ activity branch. |
| `CV_for_ion_distance` | `VoronoiD1.cpp` | `VORONOID1` | Defect-weighted distance between water O sites; contact/separation diagnostic. |
| `CV_for_ion_index` | `VoronoiIM.cpp` | `VORONOIIM` | Negative-ion index moment, weighted by squared defect. |
| `CV_for_ion_index` | `VoronoiIP.cpp` | `VORONOIIP` | Positive-ion index moment, weighted by squared defect. |
| `CV_for_ion_location_in_slab` | `VoronoiIMZ.cpp` | `VORONOIIMZ` | Negative-ion defect-weighted absolute distance from `ZMID` along `ZIDX`. |
| `CV_for_ion_location_in_slab` | `VoronoiIPZ.cpp` | `VORONOIIPZ` | Positive-ion defect-weighted absolute distance from `ZMID` along `ZIDX`. |

The corresponding archived slab input is [`Molecular_Dynamics/Enhanced_Sampling/DPMD/air_water_slab/input.plumed`](../Molecular_Dynamics/Enhanced_Sampling/DPMD/air_water_slab/input.plumed). The ion-diffusion workflow is documented in [`Ion_Diffusion_Coefficient`](../Ion_Diffusion_Coefficient).

## Common legacy interface

Every Action uses the same basic input contract:

```plumed
WaterO: GROUP ATOMS=...
WaterH: GROUP ATOMS=...

cv: VORONOIC0 GROUPA=WaterO GROUPB=WaterH NRX=0 \
    LAMBDA=-5 D_0=2 D_1=2 D_2=2 D_3=2
```

- `GROUPA` contains candidate centers, normally water O atoms.
- `GROUPB` contains transferable H atoms.
- `NRX` is the number of special sites at the **end** of `GROUPA`. For a pure water system use `NRX=0`; the extra `D_1...D_3` values are then not used by the water-only branches.
- `D_0` is the reference occupancy for the ordinary water centers. `D_1...D_3` are positional reference values for up to three special sites in the legacy kernel.
- `LAMBDA` is used as `exp(LAMBDA * distance)`. The repository examples use negative values, such as `-5`, `-8`, `-50`, and `-100`; it is not interchangeable with the positive `KAPPA` convention in the current guide.
- Periodic minimum-image distances are on by default. Add `NOPBC` only when the coordinate geometry is intentionally nonperiodic.
- `PAIR`, `SERIAL`, and `NLIST` are diagnostic/performance controls. `NLIST` requires both `NL_CUTOFF` and `NL_STRIDE`.

## Build and load as a runtime plugin

Use the same PLUMED executable and ABI as the target MD engine. From a separate build directory:

```bash
cd /path/to/OilWaterInterface/Voronoi_CVs
mkdir -p build-voronoi-water
cd build-voronoi-water

plumed mklib ../CV_for_ion_charge/VoronoiC0.cpp
plumed mklib ../CV_for_ion_charge/VoronoiC1M.cpp
plumed mklib ../CV_for_ion_charge/VoronoiC1P.cpp
plumed mklib ../CV_for_ion_distance/VoronoiD1.cpp
plumed mklib ../CV_for_ion_index/VoronoiIM.cpp
plumed mklib ../CV_for_ion_index/VoronoiIP.cpp
plumed mklib ../CV_for_ion_location_in_slab/VoronoiIMZ.cpp
plumed mklib ../CV_for_ion_location_in_slab/VoronoiIPZ.cpp
```

Compile each source separately so that each generated library has one unambiguous Action registration. Rebuild after changing PLUMED, the compiler, MPI, or the ABI.

Load the plugin before using an Action:

```plumed
LOAD FILE=./VoronoiC0.so
LOAD FILE=./VoronoiC1M.so
LOAD FILE=./VoronoiC1P.so
LOAD FILE=./VoronoiD1.so
LOAD FILE=./VoronoiIM.so
LOAD FILE=./VoronoiIP.so
LOAD FILE=./VoronoiIMZ.so
LOAD FILE=./VoronoiIPZ.so
```

The exact output suffix can differ between PLUMED versions; use the `.so` files produced by `plumed mklib`. Copying sources into `plumed/src/colvar` and rebuilding PLUMED remains an alternative for a controlled production installation.

## Engineering examples

### Bulk-water activity and separation

```plumed
LOAD FILE=./VoronoiC0.so
LOAD FILE=./VoronoiC1M.so
LOAD FILE=./VoronoiC1P.so
LOAD FILE=./VoronoiD1.so
LOAD FILE=./VoronoiIM.so
LOAD FILE=./VoronoiIP.so
LOAD FILE=./VoronoiIMZ.so
LOAD FILE=./VoronoiIPZ.so
UNITS LENGTH=A

WaterO: GROUP ATOMS=1-766:3
WaterH: GROUP ATOMS=2-767:3,3-768:3

ion_activity: VORONOIC0 GROUPA=WaterO GROUPB=WaterH NRX=0 \
  LAMBDA=-5 D_0=2 D_1=2 D_2=2 D_3=2
ion_distance: VORONOID1 GROUPA=WaterO GROUPB=WaterH NRX=0 \
  LAMBDA=-8 D_0=2 D_1=2 D_2=2 D_3=2
oh_activity: VORONOIC1M GROUPA=WaterO GROUPB=WaterH NRX=0 \
  LAMBDA=-50 D_0=2 D_1=2 D_2=2 D_3=2
h3o_activity: VORONOIC1P GROUPA=WaterO GROUPB=WaterH NRX=0 \
  LAMBDA=-50 D_0=2 D_1=2 D_2=2 D_3=2

PRINT ARG=ion_activity,ion_distance,oh_activity,h3o_activity \
  FILE=COLVAR STRIDE=1
DUMPDERIVATIVES ARG=ion_activity,ion_distance,oh_activity,h3o_activity \
  FILE=DERIVATIVES STRIDE=1
```

The atom ranges above reproduce the archived 256-water-style ordering and must be replaced when the topology changes. `VORONOIC1M` is negative for OH⁻ sites because it sums negative defects; `VORONOIC1P` is positive for H₃O⁺ sites. These are defect observables, not formal electronic charges.

### Slab location

```plumed
ion_minus_z: VORONOIIMZ GROUPA=WaterO GROUPB=WaterH NRX=0 \
  LAMBDA=-5 D_0=2 D_1=2 D_2=2 D_3=2 \
  ZIDX=2 ZMID=53
ion_plus_z: VORONOIIPZ GROUPA=WaterO GROUPB=WaterH NRX=0 \
  LAMBDA=-5 D_0=2 D_1=2 D_2=2 D_3=2 \
  ZIDX=2 ZMID=53

PRINT ARG=ion_minus_z,ion_plus_z FILE=COLVAR STRIDE=1
```

`ZIDX=0,1,2` selects x, y, or z. `ZMID` is in the active PLUMED length unit. The result is a defect-squared-weighted absolute distance, so it approaches zero when the corresponding ion defect disappears; it is not a conditional mean position.

## Important limitations

1. `VORONOIIM` and `VORONOIIP` are explicitly marked `WARNING NO DERIVATIVE!!` in the source. They are index moments using the local zero-based `GROUPA` order, not physical coordinates. Use them for post-processing diagnostics only; do not use them as bias coordinates.
2. `VORONOIIMZ` and `VORONOIIPZ` include an absolute-value cusp at `coordinate - ZMID = 0`. Check analytical derivatives around the slab midplane before biasing.
3. The legacy implementation hard-codes the ordinary/special-site split through `NRX` and the order of `GROUPA`. It does not provide the current API's explicit center vector, sign selection, physical axis, or conditional normalization.
4. `NLIST` is an approximation. The archived `NL_CUTOFF=2.4` values are water-workflow settings, not universal bond cutoffs. This legacy code has no `NL_SKIN` keyword.

## Validation sequence

Use this sequence for a new topology or parameter set:

1. Run a short `plumed driver` job without `NLIST` on representative neutral, contact-ion, separated-ion, slab-crossing, and distorted frames.
2. Check finiteness, expected signs, units, and limiting behavior when the ion defect disappears.
3. Compare values and coordinate/box derivatives against the exact mode before enabling `NLIST`.
4. Increase `NL_CUTOFF` at `NL_STRIDE=1` until the required tolerance is met, then test larger strides. Report all three NLIST parameters and the exact-mode error.
5. Use numerical derivatives only as a diagnostic; retain analytical derivatives for production biasing.
6. Record the PLUMED version, source commit, build command, atom-selection order, reference values, NLIST settings, tolerances, and plugin checksums.

## Migration to the current API

| Legacy observable | Current conceptual replacement |
| --- | --- |
| `VORONOIC0` | `VORONOI_COORDINATION ... POWER=2` |
| `VORONOID1` | `VORONOI_DISTANCE` with explicit center groups |
| `VORONOIIM/IP` | `VORONOI_POSITION` with a physical axis; avoid atom-index moments |
| `VORONOIIMZ/IPZ` | `VORONOI_POSITION` with `AXIS`, `ORIGIN`, and explicit `SIGN` |

Use the [current guide](https://zhang-pchao.github.io/code/reactive-voronoi) for new systems. Keep these files when reproducing the published water/interface workflows.

## References

- [OilWaterInterface repository](https://github.com/Zhang-pchao/OilWaterInterface)
- [Archived slab input](../Molecular_Dynamics/Enhanced_Sampling/DPMD/air_water_slab/input.plumed)
- [Ion diffusion workflow](../Ion_Diffusion_Coefficient)
- [Published interface study](https://doi.org/10.1021/acs.langmuir.4c05004)
- [Reactive Soft-Voronoi guide](https://zhang-pchao.github.io/code/reactive-voronoi)
