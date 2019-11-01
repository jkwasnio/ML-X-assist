#!/usr/bin/python

###############################################################################
# This script generates the Hamiltonian for a multi-component 1D system.
###############################################################################


import QDTK.Tools.SpfPlot as plotter
from util import discrete_eval

# import hamiltonian
from hamilt import *

## create many-body Hamiltonians and write it into files
if __name__ == "__main__":
    # plotting potentials and 1b energy levels
    energy_A, ev_A = get_diagonalized_1B_hamilt_UA()
    plotter.pot_plot(dvr, discrete_eval(U_A, xs), energy_A[0 : 4 * mA])
    energy_B, ev_B = get_diagonalized_1B_hamilt_UB()
    plotter.pot_plot(dvr, discrete_eval(U_B, xs), energy_B[0 : 4 * mB])
    # keep figures open
    pyl.show()
