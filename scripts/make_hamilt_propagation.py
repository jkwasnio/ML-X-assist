#!/usr/bin/python

###############################################################################
# This script generates the Hamiltonian for a multi-component 1D system.
###############################################################################


import os

# import hamiltonian
from hamilt import *

## create many-body Hamiltonian and write it to a file

subfolder = "propagation"
if __name__ == "__main__":
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    hamilt = get_hamilt()
    hamilt.createOperatorFileb(subfolder + "/hamilt.dat")