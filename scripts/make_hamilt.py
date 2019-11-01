#!/usr/bin/python

###############################################################################
# This script generates the Hamiltonian for a multi-component 1D system.
###############################################################################


import os

# import hamiltonian
from hamilt import *

## create many-body Hamiltonians and write it to a files
if __name__ == "__main__":
    if not os.path.exists("propagate"):
        os.makedirs("propagate")
    op1 = get_hamilt()
    op1.createOperatorFileb("propagate/hamilt.dat")
