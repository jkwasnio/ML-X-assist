#!/usr/bin/python

###############################################################################
# This script generates the Hamiltonian for a multi-component 1D system.
###############################################################################


import os

# import hamiltonian
from hamilt import get_hamilt_relax

## create many-body relaxation Hamiltonian and write it to a file
if __name__ == "__main__":
    if not os.path.exists("relax"):
        os.makedirs("relax")
    hamilt = get_hamilt_relax()
    hamilt.createOperatorFileb("relax/hamilt_relax.dat")
