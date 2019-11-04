# read-only

###############################################################################
# This script defines the Hamiltonian(s) for the multi-component 1D system.
###############################################################################


import math
import numpy as np
import pylab as pyl
import QDTK
import QDTK.Operatorb as Operb
import QDTK.Operator as Oper
import QDTK.Tools.Conversion as conv
import QDTK.PES.Potfit as pfit
import QDTK.Tools.SpfPlot as plotter
from util import discrete_eval

# import parameters
from parameters import *

# many-body Hamiltonian
def get_hamiltonian():
    """builds many body Hamiltonian for the propagation of the initial state"""
    # many-body operator -> Operatorb object

    OPER = Operb.Operatorb()
    pdim = np.zeros(2)
    pdim[0] = n
    pdim[1] = n
    OPER.pdim = tuple(pdim)
    OPER.primitive = [dvr, dvr]
    OPER.fmdegfs = 2
    OPER.symtable = (-1, 1, 3, 4)

    # Labels
    OPER.addLabel("dq2", Operb.OTerm(dvr.d2dvr))
    OPER.addLabel("UA", Operb.OTerm(discrete_eval(U_A, xs)))
    OPER.addLabel("UB", Operb.OTerm(discrete_eval(U_B, xs)))
    OPER.addLabel("delta", Operb.OTerm(dvr.delta_w()))

    OPER.addLabel("kin1", Operb.OCoef(-0.5 / massA))
    OPER.addLabel("kin2", Operb.OCoef(-0.5 / massB))
    OPER.addLabel("one", Operb.OCoef(1.0))
    OPER.addLabel("gAB", Operb.OCoef(gAB))

    tab = """
## 1body terms
## Kinetic Energy
kin1        |1 dq2
kin2        |2 dq2
## trap
one         |1 UA
one         |2 UB

## interaction
gAB         |{1:2} delta

"""
    OPER.readTableb(tab)

    return OPER


# one-body Hamiltonian for species \sigma
def get_1B_hamiltonian_A():
    """ returns 1body Hamiltonian defined by trapping potential U"""
    # 1body Hamiltonian constructed as an Operator, not Operatorb object in
    # order not to care about the shaddow terms

    OPER = Oper.Operator()  #### OPER is defined as a Operator class in Oper
    pdim = np.zeros(1)
    pdim[0] = n
    OPER.pdim = tuple(pdim)
    OPER.primitive = [dvr]

    # Labels
    OPER.addLabel("dq2", Oper.OTerm(dvr.d2dvr))
    OPER.addLabel("UA", Oper.OTerm(discrete_eval(U_A, xs)))

    OPER.addLabel("kin1", Oper.OCoef(-0.5 / massA))
    OPER.addLabel("one", Oper.OCoef(1.0))

    tab = """
## Kinetic Energy
kin1        |1 dq2
## double well trap
one         |1 UA
"""
    OPER.readTable(tab)

    return OPER


def get_1B_hamiltonian_B():
    """ returns 1body Hamiltonian defined by trapping potential U"""
    # 1body Hamiltonian constructed as an Operator, not Operatorb object in
    # order not to care about the shaddow terms

    OPER = Oper.Operator()  #### OPER is defined as a Operator class in Oper
    pdim = np.zeros(1)
    pdim[0] = n
    OPER.pdim = tuple(pdim)
    OPER.primitive = [dvr]

    # Labels
    OPER.addLabel("dq2", Oper.OTerm(dvr.d2dvr))
    OPER.addLabel("UB", Oper.OTerm(discrete_eval(U_B, xs)))

    OPER.addLabel("kin2", Oper.OCoef(-0.5 / massB))
    OPER.addLabel("one", Oper.OCoef(1.0))

    tab = """
## Kinetic Energy
kin2        |1 dq2
## double well trap
one         |1 UB
"""
    OPER.readTable(tab)

    return OPER
