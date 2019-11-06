# ML-X-assist

## Guides
### Initialization of Setups (Example)
#### Step 1:
Configure the [`parameters.py`](init/parameters.py) and [`hamiltonian.py`](init/hamiltonian.py) in the [`./init`](init) folder to match the properites of a general setup. Edit the content of the job scripts for each stage as well ([`init_relaxation/job.sh`](init_relaxation/job.sh)/[`init_propagation/job.sh`](init_propagation/job.sh)).
#### Step 2:
```
./scripts/make_setupdirs 2
```
creates two setup folders in `./setups` with ids `1` and `2` (folder names).
```
./scripts/make_stage_dirs relaxation
./scripts/make_stage_dirs propagation
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


### Working with MATLAB
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "make_parameters_mat"
```
creates the `parameters.mat` file which is a MATLAB-readable version of the `parameters.py`.

_Note: Not all values are transfered._

```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "run_matlab_script example.m"
```
runs the MATLAB script `example.m` located in `./scripts/matlab`.

_Note: The script must begin with a change to the current working directory and might load the parameters.mat (see [`./scripts/matlab/template.m`](scripts/matlab/template.m))._

## Make Scripts Executable
To make all scripts executable call
```
cd ./scripts
chmod u+rwx *
```
or replace `*` by the name of the script to make a single script executable.
