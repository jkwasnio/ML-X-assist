# read-only

################################################################################
### These are the physical and mathematical parameters.                      ###
### All scripts treat these values as read only.                             ###
### WARNING: DO NOT change these between running scripts or the output is    ###
###          undefined.                                                      ###
################################################################################

import math
import QDTK


### physical parameters ###

## particle numbers
# number of species
Ns = 2
# number of particles in species \sigma
NA = 1
NB = 1

## masses
# particle mass of species \sigma
massA = 1.0
massB = 1.0

## potentials
# frequency of the harmonic potential A
omegA = 0.1
# height of gaussian peak in potential A
hA = 1.0
# width  of gaussian peak in potential A
wA = 1.0
# frequency of the harmonic potential B
omegB = 0.1
# formulas for trapping potentials of species \sigma
# trapping potential U_\sigma for species \sigma
U_A = lambda x: 0.5 * massA * (omegA ** 2) * (x ** 2) + hA * math.exp(
    -x ** 2 / (2 * wA ** 2)
) / (wA * math.sqrt(2 * math.pi))

U_B = lambda x: 0.5 * massB * (omegB ** 2) * (x ** 2)

## interaction
# AB interspecies interaction strengths
gAB = 1

## time
# final time (inclusive)
tfinal = 100
# time step
dt = 0.1


### mathematical parameters ###

## dvr & its parameters (harmonic dvr is used)
# hard wall boundaries
xmin = -25
xmax = 25
# number of dvr gridpoints
n = 300
# sin dvr
dvr = QDTK.sdvr(n, xmin, xmax)
xs = dvr.x

## parameters of wave function expansion
# number of \sigma species states
MA = 6
MB = 6
# number of \sigma single particle functions
mA = 6
mB = 6
