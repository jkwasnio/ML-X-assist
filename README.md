# ML-X-assist

## Example
Configure the `parameters.py` and `hamiltonian.py` in the `./init` folder t match the properites of a general setup.

Call 
```
./scripts/make_setupdirs 2
```
to create two setup folders in `./setup` with ids `1` and `2` (folder names).


Call 
```
./scripts/make_stage_dirs relaxation
```
and
```
./scripts/make_stage_dirs propagation
```
to create subdirectories for the relaxation and propagation stage.

Call 
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "init init gAB={ID}-1"
```
and
```
./scripts/exec_script_in_stage_in_all_setupdirs propagation "init init gAB={ID}-1;hA=0"
```
to copy the content of the `./init` folder (`parameters.py` and `hamiltonian.py`) to each setup. Here, in `parameters.py` each `gAB` is set to the value of the setup id minus one and `hA` is set to zero during the propagation.


Call 
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "make_hamiltonian"
```
and
```
./scripts/exec_script_in_stage_in_all_setupdirs propagation "make_hamiltonian"
```
to generate the Hamiltonians in each setup for the relaxation and propagation respectively.


Call 
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "make_initial_wavefunction_for_relaxation"
```
to create the initial wavefunction for the relaxation.

### Working with MATLAB
Call 
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "make_parameters_mat"
```
to create the `parameters.mat` file which is a MATLAB-readable version of the `parameters.py`.

_Note: Not all values are transfered._

Call 
```
./scripts/exec_script_in_stage_in_all_setupdirs relaxation "run_matlab_script example.m"
```
to run the MATLAB script `example.m` located in `./scripts/matlab`.

_Note: The script must begin with a change to the current working directory and might load the parameters.mat (see `./scripts/matlab/template.m`)._

## Make Scripts executable
```
cd ./scripts
chmod u+rwx *
```
