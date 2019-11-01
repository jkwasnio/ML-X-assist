#!/usr/bin/python

###############################################################################
# This script generates the Hamiltonian for a multi-component 1D system.
###############################################################################


import QDTK.Tools.SpfPlot as plotter
from util import discrete_eval

# import hamiltonian
from hamilt import get_1B_hamilt_UA, get_1B_hamilt_UB

# plotting potentials and 1b energy levels
if __name__ == "__main__":
    # get 1b hamiltonians (potential term only)
    hamilt_1b_UA = get_1B_hamilt_UA()
    hamilt_1b_UB = get_1B_hamilt_UB()
    # calculate eigenvalues
    eigen_energies_A, eigen_states_A = hamilt_1b_UA.diag_1b_hamiltonian1d(n)
    eigen_energies_B, eigen_states_B = hamilt_1b_UB.diag_1b_hamiltonian1d(n)
    # plot
    plotter.pot_plot(dvr, discrete_eval(U_A, xs), eigen_energies_A[0 : 4 * mA])
    plotter.pot_plot(dvr, discrete_eval(U_B, xs), eigen_energies_B[0 : 4 * mB])
    # keep figures open
    pyl.show()
