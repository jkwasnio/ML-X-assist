#!/usr/bin/python

###############################################################################
# This script generates the Hamiltonian for a multi-component 1D system.
###############################################################################


import os

# import hamiltonian
from hamilt import get_hamilt_relax

## create many-body relaxation Hamiltonian and write it to a file

subfolder = "relaxation"
if __name__ == "__main__":
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    hamilt = get_hamilt_relax()
    hamilt.createOperatorFileb(subfolder + "/hamilt.dat")