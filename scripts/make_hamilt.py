#!/usr/bin/python

###############################################################################
# This script generates the Hamiltonian for a multi-component 1D system.
###############################################################################


# import hamiltonian
from hamilt import *

## create many-body Hamiltonians and write it to a files
if __name__ == "__main__":
    op1 = get_hamilt()
    op1.createOperatorFileb("hamilt.dat")
