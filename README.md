# ML-X-assist

ML-X-assits is a set of scripts to assist handling multiple related ML-X setups with one or more stages. It provides scripts for basic stage manipulations (initialize, relaxation or propagation locally or remotely) and thier batched execution. In addition customizable configuration files and template files are provided.

This documentation has the following structure:
- [Terminology](#terminology) explains terms used in this document
- [File-Structure](#file-structure) gives an overview of purposes of direcotries and locations of files
- [Guides](#guides) provide a walk-through guides of all common tasks as an example
  - [Initialization of Setups](#initialization-of-setups)
  - [Run Jobs](#run-jobs)
  - [Run Jobs Remotely](#run-jobs-remotely)
  - [Working with MATLAB](#working-with-matlab)
- [Scripts](#scripts) lists all important scripts and their purposes
- [Appendix](#appendix)

## Terminology

The following terms are used throughout this documentation:

| Term | Explanation |
|------|-------------|
| setup | a single simulated experiment (e.g. a trap with fixed potentials and particle properties)|
| stage | a single step in a setups development (e.g. relaxation or propagation); some properties might change from one stage to another (quench) |

## File Structure

Files are organized according to this structure:

```
 o ML-X-assits               (the root directory; the name of this directory can be customized)
 +---o init                  (template files used to initialize any stage)
 |   +---o hamiltonian.py    (file to configure single particle and multi-species hamiltonians; usually identical for all setups)
 |   +---o parameters.py     (template for all parameters of the setup; will change slightly form setup to setup)
 |   +---o job_remote.sh     (template to run the job.sh from the cluster; optional)
 |
 +---o init_<stage_1>        (template files specific to <stage_1> only)
 |   +---o job.sh            (template for the stages job; e.g. calls the relaxation or propagation procedure of ML-X)
 |
 +---o init_<stage_2>        (template files specific to <stage_2> only)
 |   +---o ...
 |
 +--o ...
 |
 +---o scripts               (root directory for all scripts of ML-X-assist)
 |   +---o ...               (see Sec. Scripts for more details)
 |
 +---o setups                (directory for for all setups)
     +---o 1                 (directory of first setup)
     |   +---o <stage_1>     (one directory for each stage)
     |   |   +---o ...       (files of <stage_1>) 
     |   |
     |   +---o <stage_2>
     |   |   +---o ...
     |   |
     |   + ...
     |
     +---o 2                 (directory of second setup)
     |   +---o <stage_1>
     |   |   +---o ...
     |   |
     |   +---o <stage_2>
     |   |   +---o ...
     |   |
     |   + ...
     |
     + ...
```

## Guides

This section contains a walk-through guide on how to use ML-X assist.

### Initialization of Setups

#### Step 1:
Configure the [`parameters.py`](init/parameters.py) and [`hamiltonian.py`](init/hamiltonian.py) in the [`./init`](init) folder to match the properites of a general setup. Edit the content of the job scripts for each stage as well ([`init_relaxation/job.sh`](init_relaxation/job.sh)/[`init_propagation/job.sh`](init_propagation/job.sh)).

#### Step 2:
```
./scripts/make_setupdirs 2
```
creates two setup folders in `./setups` with ids `1` and `2` (folder names).
```
./scripts/make_stagedirs relaxation
./scripts/make_stagedirs propagation
```
creates subdirectories for the relaxation and propagation stage.

#### Step 3
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "init init gAB={ID}-1"
./scripts/exec_script_in_stage_in_all_setupdirs propagation "init init gAB={ID}-1;hA=0"
```
runs the script [`./scripts/init`](scripts/init) in the stage folder `relaxation`/`propagation` for all setups. [`./scripts/init`](scripts/init) copies the content of the [`./init`](init) folder ([`parameters.py`](init/parameters.py) and [`hamiltonian.py`](init/hamiltonian.py)) to each setup. Here, in [`parameters.py`](init/parameters.py)each `gAB` is set to the value of the setup id minus one and `hA` is set to zero during the propagation.

_Note: The content of [`./init_relaxaion`](init_relaxation) resp. [`./init_propagation`](init_propagation) is copied as well if such a folder exists. In addition all parameter references (`{PARAMETER_NAME}`) are resolved inside these files as well._

#### Step 4
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "make_hamiltonian"
./scripts/exec_script_in_stage_in_all_setupdirs propagation "make_hamiltonian"
```
generates the Hamiltonians in each setup for the relaxation and propagation respectively.

#### Step 5
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "make_initial_wavefunction_for_relaxation"
```
creates the initial wavefunction for the relaxation.

### Run Jobs
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "file_edit job.sh job.sh ML_X_PATH=~/ML-X"
./scripts/exec_script_in_stage_in_all_setupdirs propagation "file_edit job.sh job.sh ML_X_PATH=~/ML-X"
```
sets the ML-X path for the relaxation and propagation.

_Note: Replace `~/ML-X` with the actual path to the ML-X root folder._

```
./scripts/exec_in_stage_in_all_setupdirs relaxation "bash job.sh"
./scripts/exec_in_stage_in_all_setupdirs propagation "bash job.sh"
```
runs the relaxation/propagation script in all setups sequentially.

### Run Jobs Remotely
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "file_edit job_remote.sh job_remote.sh \"SGE_JOB_QUEUE=QUEUE;SGE_JOB_MAIL_ADDRESS=USERNAME@DOMAIN.COM;SGE_JOB_MAIL_OPTIONS=ea;SGE_JOB_MEM_LIMIT_GB=4;SGE_JOB_TIME_LIMIT_H=1;SGE_JOB_NAME=JOBNAME;SGE_JOB_ORDER_COMMAND=;SGE_JOB_PREAMBLE=\""
./scripts/exec_script_in_stage_in_all_setupdirs propagation "file_edit job_remote.sh job_remote.sh \"SGE_JOB_QUEUE=QUEUE;SGE_JOB_MAIL_ADDRESS=USERNAME@DOMAIN.COM;SGE_JOB_MAIL_OPTIONS=ea;SGE_JOB_MEM_LIMIT_GB=4;SGE_JOB_TIME_LIMIT_H=1;SGE_JOB_NAME=JOBNAME;SGE_JOB_ORDER_COMMAND=;SGE_JOB_PREAMBLE=\""
```
edits the file [`./init/job_remote.sh`](init/job_remote.sh).

_Note: Insert your desired values for `QUEUE`, `USERNAME@DOMAIN.COM` and `JOBNAME` and adapt the memory (`SGE_JOB_MEM_LIMIT_GB`) and time limits (`SGE_JOB_TIME_LIMIT_H`) if needed._

__Important Note: Enquote e-mail addresses and avoid spaces (or `qsub` will not accept the jobs)!__

Call
```
./scripts/exec_in_stage_in_all_setupdirs relaxation "qsub job_remote.sh"
```
and after all jobs are finished
```
./scripts/exec_in_stage_in_all_setupdirs propagation "qsub job_remote.sh"
```
to submit the jobs to the SGE system.

### Working with MATLAB
```
./scripts/exec_script_in_stage_in_all_setupdirs propagation "make_parameters_mat"
```
creates the `parameters.mat` file which is a MATLAB-readable version of the `parameters.py`.

_Note: Not all values are transfered._

```
./scripts/exec_script_in_stage_in_all_setupdirs propagation "run_matlab_script example.m"
```
runs the MATLAB script `example.m` located in `./scripts/matlab`.

_Note: The script must begin with a change to the current working directory and might load the parameters.mat (see [`./scripts/matlab/template.m`](scripts/matlab/template.m))._

#### Extract and Display One-Body Data (In Real Space)
Several auxiliar files must be created __in the following order__ first to change the representation from raw ASCII data in an ML-X-internal format (`psi`, `gpop`, `natpop`, ...) to MATLAB-friendly .MAT files representing one-body densities in real space:

| Step | File | Command | Comment |
|-----:|:-----|:--------|---------|
| 1 | `parameters.mat` | `./scripts/exec_script_in_stage_in_all_setupdirs propagation make_parameters_mat` | MATLAB-readable version of `parameters.py` ; same as in Sec. [Working with MATLAB](#working-with-matlab)
| 2 | `psi.mat` | `scripts/exec_script_in_stage_in_all_setupdirs propagation "OutpurSTD.py --psi"` | wavefunction data `psi` (ASCII) to .MAT
| 3 | `tape.mat` | `./scripts/exec_script_in_stage_in_all_setupdirs propagation "run_matlab_script \"makeTapeMat.m\""` | general parameters extracted from PSI file
| 4 | `diag_top.mat` | `./scripts/exec_script_in_stage_in_all_setupdirs propagation "run_matlab_script \"makeDiagTopMat.m\""` | natural species functions and their populations
| 5 | `density1b.mat` | `./scripts/exec_script_in_stage_in_all_setupdirs propagation "run_matlab_script \"makeDensity1bMat.m\""` | one-body densities in working orbitals
| 6 | `gpop.mat` `dmat1A_grid.mat` `dmat1B_grid.mat` | `./scripts/exec_script_in_stage_in_all_setupdirs propagation "run_matlab_script \"makeMBOneBodyDensityData.m\""` | one-body densities in real space (grid)

After step 6, the transformed data is stored in files `gpop.mat`, `dmat1A_grid.mat` and `dmat1B_grid.mat`.


## Scripts
There are three major categories of scripts provided by ML-X-assits:
- Setups Initializing Scripts: create directories for setups and stages only
- Stage Maipulating Scripts: operate in in a single stage
- Multiplexer Scripts: execute commands or scripts in multiple setups/stages consecutively; begin with `exec_` prefix

Descriptions of the most important scripts are given below. See [`scripts`](scripts) for all scripts available.

### Setups Initializing Scripts
Initialize the directories of the setups/stages.
- Operate on ML-X root level.
- **No change of directory required**.

| Script Call | Purpose |
|:-------|:--------|
| `.scripts/make_setupdirs <n>` | create `<n>` setup directories labeled `1`, `2`, ... `<n>`, `<n>` *must be a positive integer* |
| `.scripts/make_stagedirs <stage>` | create `<stage>` directory in each setup |

### Stage Manipulating Scipts
These scripts handle a single task performed on a stage.
- Operate on stage level.
- **Change directory manually** to the desired stage prior to any script call.

| Script Call | Purpose |
|:-------|:--------|
| `../../scripts/init init "<attribute_1>=<expression_1>;...;<attribute_n>=<expression_n>"` | copy all files from `init` and overwrite any occurences of `<attribute_i>` in `parameters.py` with `<expression_i>` in `parameters.py` and all files copied from the corresponding `init_<stage>` folder; see [this example](#step-3) |
| `../../scripts/make_hamiltonian` | create `hamiltonian.dat` |
| `../../scripts/visualize_1b_hamiltonian` | display the one-bdy hamiltonians and their lowest eigenenergies |
| `../../scripts/make_initial_wavefunction_for_relaxation` | create an initial guess of a wavefunction of the entire system `initial_wavefunction.dat` which is assumed to be **near** a  ground state |
| `../../scripts/make_parameters_mat` | create `parameters.mat` which converts all simple data types (int, float, string, etc. ) from `parameters.mat` to a .MAT file |
| `../../scripts/run_matlab_script <matlabscript.m>` | run a script located at `scripts/matlab/<matlabscript.m>` within the current terminal (exits MATLAB automatically after script finished or raised an exception) |
| `../../scripts/OutPutSTD.py --psi` | converts `psi` to `psi.mat` |

### Multiplexer Scripts
These scripts apply a manipulation suitable for a single setup/stage to multiple stetups/stages consecutively.
- Operate on ML-X-assits root level.
- No maunual change of directory required since each **script changes directory to the setup/stage directory it is operatng in**.

| Script Call | Purpose |
|:-------|:--------|
| `exec_in_all_setupdirs "<command>"` | execute `<command>` in each setup directory |
| `exec_in_stage_in_all_setupdirs <stage> "<command>"` | execute `<command>` in each `<stage>` directoy in each setup directory |
| `exec_script_in_all_setupdirs "<command>"` | execute `<path_to_scripts>/<command>` in each setup directory |
| `exec_script_in_stage_in_all_setupdirs <stage> "<command>"` | execute `<path_to_scripts>/<command>` in each `<stage>` directoy in each setup directory |

The scripts prefixed with `exec_script_` have the advantage to automatically insert the path of the `scripts` folder in front of the `<command>`.

## Appendix

### Make Scripts Executable
To make all scripts executable call
```
cd ./scripts
chmod u+rwx *
```
or replace `*` by the name of the script to make a single script executable.
