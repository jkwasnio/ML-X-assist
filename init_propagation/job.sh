#!/bin/bash


{ML_X_PATH}/Bin/qdtk_propagate.x -rst initial_wavefunction.dat -opr hamiltonian.dat -dt {dt} -tfinal {tfinal} -itg dp5 -atol 1e-12 -psi -rstzero
