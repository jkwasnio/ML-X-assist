#!/usr/bin/python

###############################################################################
# This script generates the initial wavefunction for a multi-component 1D
# system. The initial state is supposed to be of the form:
#
#   |\Psi(t=0)> = \prod_\sigma |ns_\sigma>_\sigma,
#
# where |ns_\sigma>_\sigma is an arbitrary number state of the species \sigma.
# For each such number state, the user has to provide as many SPFs as orbitals
# are occupied.
###############################################################################

import numpy as np
import pylab as pyl

import QDTK
import QDTK.Wavefunction as Wavefunction
import QDTK.Tools.Mathematics as Mathematics
import QDTK.Tools.SpfPlot as SpfPlot

from make_hamilt import (
    get_diagonalized_1B_hamilt_UA,
    get_diagonalized_1B_hamilt_UB,
)

# import parameters
from parameters import *

if __name__ == "__main__":
    tape = (
        -10,
        2,
        0,
        MA,
        MB,
        -1,
        1,
        NA,
        -1,
        mA,
        -1,
        1,
        1,
        0,
        n,
        0,
        0,
        -1,
        2,
        NB,
        -1,
        mB,
        -1,
        1,
        1,
        0,
        n,
        -2,
    )

    # initial number states populations
    ns_A = np.zeros(mA, int)
    ns_B = np.zeros(mB, int)
    ns_A[0:NA] = 1
    ns_B[0:NB] = 1
    # bundle initial number states populations
    ns = [ns_A, ns_B]

    # eigenstates and values of ititial potentials
    energiesA, eigenstatesA = get_diagonalized_1B_hamilt_UA()
    energiesB, eigenstatesB = get_diagonalized_1B_hamilt_UB()
    #
    SPF_A = Wavefunction.grab_lowest_eigenfct(mA, eigenstatesA)
    SPF_B = Wavefunction.grab_lowest_eigenfct(mB, eigenstatesB)
    # orthonormalize 1body eigenstates for safety
    Mathematics.gramSchmidt(SPF_A)
    Mathematics.gramSchmidt(SPF_B)
    # bundle SPFs
    SPF = [SPF_A, SPF_B]
    # plot SPFs
    # SpfPlot.spf_plot(dvr,SPF_A)
    # pyl.show()

    # create initial wavefunction
    # accuracies for normalization and orthogonality
    eps_norm = 10 ** (-15)
    eps_over = 10 ** (-15)
    wfn = QDTK.Wfn(tape=tape)
    wfn.init_coef_multi_spec(Ns, ns, SPF, eps_norm, eps_over, full_spf=True)
    # write wavefunction to file
    wfn.createWfnFile("initial_wfn.dat")
