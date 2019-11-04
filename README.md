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
./scripts/exec_script_in_all_setupdirs "make_hamilt_relaxation.py"

```
and
```
./scripts/exec_script_in_all_setupdirs "make_hamilt_propagation.py"

```
to generate the Hamiltonians in each setup for the relaxation and propagation respectively.


Call 
```
./scripts/exec_script_in_all_setupdirs "make_initial_wavefunction.py"

```
to create the initial wavefunction for the relaxation.

## Make Scripts executable
```
cd ./scripts
chmod u+rwx *
```
