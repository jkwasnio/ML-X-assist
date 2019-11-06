#!/bin/bash

{ML_X_PATH}/Bin/qdtk_propagate.x -rst initial_wavefunction.dat -opr hamiltonian.dat -dt 1.0 -tfinal 5000.0 -itg dp5 -atol 1.d-12 -rtol 1.d-12 -reg 1.d-7 -psi -rstzero -resetnorm -gramschmidt -relax -statsteps 1 -stat_energ_tol 1.0e-9 -stat_npop_tol 1.0e-9
