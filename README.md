# ML-X-assist

## Example
Configure the `parameters.py` and `hamilt.py` in the `./init` folder t match the properites of a general setup.

Call 
```
./scripts/make_setupdirs 2
```
to create two setup folders in `./setup` with ids `1` and `2` (folder names).


Call 
```
./scripts/exec_script_in_all_setupdirs "init gAB={ID}-1;"
```
to copy the content of the `./init` folder (`parameters.py` and `hamilt.py`) to each setup. Here, in `parameters.py` each `gAB` is set to the value of the setup id minus one.


Call 
```
./scripts/exec_script_in_all_setupdirs "make_hamilt_relaxation"
```
and
```
./scripts/exec_script_in_all_setupdirs "make_hamilt_propagation"
```
to generate the Hamiltonians in each setup for the relaxation and propagation respectively.


Call 
```
./scripts/exec_script_in_all_setupdirs "make_initial_wavefunction_relaxation"
```
to create the initial wavefunction for the relaxation.

### Working with MATLAB
Call 
```
./scripts/exec_script_in_all_setupdirs "make_parameters_mat"
```
to create the `parameters.mat` file which is a MATLAB-readable version of the `parameters.py`.

_Note: Not all values are transfered._

Call 
```
./scripts/exec_script_in_all_setupdirs "run_matlab_script example.m"
```
to run the MATLAB script `example.m` located in `./scripts/matlab`.

_Note: The script must begin with a change to the current working directory and might load the parameters.mat (see ./scripts/matlab/template.m`)._

## Make Scripts executable
```
cd ./scripts
chmod u+rwx *
```
