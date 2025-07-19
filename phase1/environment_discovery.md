# Phase 1: Environment Discovery Report

## Executive Summary
This report details the comprehensive discovery of the Ares computing cluster environment, including filesystem resources, compute infrastructure, hardware specifications, and available software modules.

## 1. Filesystem and Scientific Data Discovery

### Available Scientific Datasets
The `/mnt/common` filesystem contains extensive scientific computing resources:

#### Genomics and Bioinformatics
- **1000 Genome Project Data** (`/mnt/common/datasets/1000-genome/`)
  - Multiple release versions (2008_12, 2009_02, 2009_04, 2009_05, 2009_08, 20100804)
  - CEU, YRI, and JPTCHB population datasets
  - SNP and indel call data in various formats (.gz, .vcf)

#### Weather and Climate Modeling
- **TeraFusion datasets** (`/mnt/common/datasets/TeraFusion/`)
- **FlexTRKR tracking data** (`/mnt/common/datasets/flextrkr/`)
  - PyFLEXTRKR manuscript data (2022)
  - NEXRAD reflectivity data
  - Sample datasets (20230517)

#### Molecular Dynamics and Materials Science
- **DeepDriveMD datasets** (`/mnt/common/datasets/deepdrivemd/`)
- **MyRA simulation data** (`/mnt/common/datasets/MyRA/`)
- **VASP calculations** (H2O-1024p datasets)

#### I/O and Performance Analysis
- **Darshan I/O traces** (`/mnt/common/datasets/Darshan_traces/`)
- **Beacon tracing data** (`/mnt/common/datasets/Beacon_traces/`)

#### User Research Projects
- Extensive user directories containing:
  - LAMMPS molecular dynamics simulations
  - WRF weather modeling
  - OpenFOAM fluid dynamics
  - HDF5 and ADIOS2 I/O benchmarks
  - Hermes storage system data

## 2. Slurm Cluster Status and Resources

### Cluster Configuration
- **Cluster Name**: slurm-cluster
- **Slurm Version**: 21.08.5
- **Total Nodes**: 32 compute nodes (ares-comp-01 through ares-comp-32)

### Node Status Summary
- **Idle Nodes**: 17 nodes available for scheduling
  - ares-comp-[06,08,10,12,14,16,18,19,21,23,25,27,28,29,30,31,32]
- **Down Nodes**: 13 nodes currently offline
  - ares-comp-[01,02,04,05,07,09,11,15,17,20,22,24,26]
- **Drained Nodes**: 2 nodes administratively disabled
  - ares-comp-[03,13]

### Partition Configuration
- **Partition**: compute
- **Time Limit**: 2 days (2-00:00:00)
- **Current Queue**: Empty (0 running/pending jobs)

### Available Computing Resources
- **Available CPUs**: 680 cores (17 idle nodes × 40 cores each)
- **Total Theoretical Capacity**: 1,280 cores (32 nodes × 40 cores each)
- **Current Utilization**: 0% (no running jobs)

## 3. Hardware Specifications

### Current Node Hardware (Login/Compute Node)
- **CPU**: Intel(R) Xeon(R) Silver 4114 @ 2.20GHz
  - **Architecture**: x86_64
  - **Sockets**: 2
  - **Cores per Socket**: 10
  - **Threads per Core**: 2
  - **Total Logical CPUs**: 40
  - **Cache**: L1d: 640 KiB, L1i: 640 KiB, L2: 20 MiB
  - **Features**: AVX-512, Intel VT-x, Hardware Security (Intel PT, MPX)

- **Memory**: 94 GiB total RAM
  - **Available**: 83 GiB free
  - **Swap**: 8.0 GiB
  - **Current Usage**: ~9 GiB used (10% utilization)

- **Storage**: 
  - **Root Filesystem**: 1007 GiB total, 662 GiB available (31% used)
  - **Shared Storage**: Extensive `/mnt/common` with scientific datasets

## 4. Software Environment and Modules

### Module Systems Available
- **Lmod**: Successfully configured and functional
- **Multiple Module Paths**:
  - Spack-managed modules (primary)
  - Repository software modules
  - User-specific modules

### Key Scientific Software Available

#### High-Performance Computing Libraries
- **MPI**: OpenMPI 5.0.5
- **Compilers**: GCC 11.4.0
- **Build Systems**: CMake 3.30.5, Autotools suite

#### I/O and Data Management
- **ADIOS2**: Multiple versions (2.9.0, 2.10.2) with MPI support
- **HDF5**: Versions 1.14.0, 1.14.5 (parallel-enabled)
- **NetCDF**: NetCDF-C 4.9.2, NetCDF-Fortran 4.6.1
- **Parallel-NetCDF**: 1.12.3

#### Storage and I/O Systems
- **Hermes**: 1.2.1 (distributed storage system)
- **OrangeFS**: 2.9.8, 2.10 (parallel filesystem)
- **Darshan**: 3.4.6 (I/O characterization)

#### Scientific Applications
- **LAMMPS**: 20240829.1 (molecular dynamics)
- **WRF**: 4.6.1 (weather modeling)
- **OpenFOAM**: 2312 (computational fluid dynamics)
- **ParaView**: 5.13.1 (visualization)
- **Montage**: 6.0 (astronomical image processing)

#### Data Analysis and Compression
- **Python**: 3.11.9, 3.13.0 with scientific stack
- **Compression**: zstd, lz4, bzip2, sz (lossy compression)
- **Arrow**: 15.0.1 (columnar data format)

#### Performance and Debugging Tools
- **IOWarp**: I/O workload analysis and replay
- **IOR**: 3.3.0 (I/O benchmarking)
- **Jarvis-CD**: Continuous delivery for HPC

#### Specialized Research Tools
- **MGARD**: Error-bounded lossy compression
- **Mercury/Margo/Thallium**: High-performance RPC framework
- **Chi-nettest**: Network testing framework

## 5. Environment Assessment Summary

### Strengths
1. **Rich Scientific Dataset Repository**: Extensive collection covering genomics, climate, materials science
2. **Modern Software Stack**: Up-to-date versions of key HPC software
3. **Diverse I/O Ecosystem**: Multiple storage systems and I/O libraries available
4. **Comprehensive Module System**: Well-organized software environment via Spack/Lmod

### Current Limitations
1. **Reduced Compute Capacity**: 59% of nodes currently unavailable (15 down/drained)
2. **No Active Workload**: Cluster currently idle, may indicate maintenance period

### Recommendations for Scientific Computing
1. **Data-Intensive Workflows**: Excellent support for genomics, climate, and molecular dynamics
2. **I/O Performance Studies**: Rich ecosystem for storage system research
3. **Multi-Scale Simulations**: Good support for coupled simulations across disciplines
4. **Workflow Development**: Strong foundation for scientific workflow automation

### Next Steps
1. Verify node availability and maintenance schedules
2. Test job submission and resource allocation
3. Validate data access patterns and performance
4. Establish baseline performance metrics

---
*Generated on 2025-07-19 as part of Phase 1 Environment Discovery*