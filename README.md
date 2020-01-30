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
