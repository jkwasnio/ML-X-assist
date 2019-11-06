#!/usr/bin/env python

"""
OutputSTD
=========
:Abstract:
	The file contains functions which do some small helper task

:Authors:
	- S. Kroenke   skroenke@physnet.uni-hamburg.de (SK)
        - J. Schurer   jschurer@physnet.uni-hamburg.de (JS)

:Version:
	0.1 of 28.07.2015
	
:Status:
	To be tested

:Content:
	- CUTPSI(FileName,FileOut) by SK (Tested)
	- PHASE_IMPRINT(FileName,FileOut) by JS (Tested)

:History:
	- 28.07.2015 JS sets up this file
        - 16.12.2015 JS add PHASE_IMPRINT

		
:License:	
	
:Notes:
	
"""

import scipy.io as scIo
from numpy import reshape, array,tanh
import numpy as np
from optparse import OptionParser
import sys
import os
from warnings import  filterwarnings
from math import sqrt,pi
filterwarnings("ignore", category=FutureWarning) 
import subprocess

########################################################################
####	 Small Helper Routines


###################
####	CUTPSI 	########
###################
def CUTPSI(FileName, FileOut,T,T0=10.01):
	"""This small prog deletes all entries of a psi file for times larger than T 
and extracts the restart file corresponding to T
"""
	
        frst_out  = 'restart_cutted' #output restart file

        #OPEN Files
        try: PSI_IN  = open(FileName,'r')
        except: raise ValueError(FileName +' not found')
        try: PSI_OUT = open(FileOut,'w')
        except: raise ValueError(FileOut +' not found')
        try: RST_OUT = open(frst_out,'w')
        except: raise ValueError(frst_out +' not found')

        psi_zero= []
        in_tape = False
        in_psi  = False
        in_psi0 = False
        in_psit = False
        last_t  = False
        t       = None

        for line in PSI_IN:
            if '$tape' in line:
                in_tape = True
            if '$time' in line:
                if last_t: break     # perform cut
                in_tape = False
                in_psi  = True
            if '[au]' in line:
                t = float(line.split('[au]')[0])
                print 'time', t
                if t==T:    
                    last_t = True
                    RST_OUT.write('$time \n')
    
            if in_tape:
                PSI_OUT.write(line)
                RST_OUT.write(line)
        
            if not in_psi: continue
    	    if t >= T0:
            	PSI_OUT.write(line)
            if last_t:
                RST_OUT.write(line)
        
            if t==T0:
                in_psi0 = True
            else:
                in_psi0 = False
        
            if in_psi0:
                psi_zero.append(line)

        RST_OUT.write('\n$psi_zero\n')
        for line in psi_zero:
            if '$psi' in line: continue
            if '$time' in line: continue
            if '[au]' in line: continue
            RST_OUT.write(line)

        #Close
        PSI_IN.close()
        PSI_OUT.close()
        RST_OUT.close()

	print "\t{x} saved".format(x=FileOut)
	print "\t{x} saved".format(x=frst_out)


###################
####	Phase Imprint of SPFs 	########
###################
def PHASE_IMPRINT(FileNameRST,FileNameHamilt, FileOut,node,func,funcPar):
	"""The tool multiplys a spatial dependent phase onto the SPFs 
"""

        cmd = "OutputSTD.py --psi -i " + FileNameRST
        out_str = subprocess.check_output(cmd, shell=True)
        cmd = "OutputSTD.py --oper -i " + FileNameHamilt
        out_str = subprocess.check_output(cmd, shell=True)

        RST = scIo.loadmat('{x}.mat'.format(x=FileNameRST))
        GRID = scIo.loadmat('{x}.mat'.format(x=FileNameHamilt))

        newTape = RST['tape'][0]
        SPFs = RST['node'+ str(int(node))]
        m = SPFs.shape[1]
        n = SPFs.shape[2]
        x = GRID['grid']

        # Get imprint function
        if (func=='lin'):#Linear
             phase = funcPar[0]*np.pi*x
        if (func=='tanh'):#tanh
             phase = funcPar[0]*np.pi/2.0*tanh(x/(2.0*funcPar[1]))
        
        #Imprint     
        SPFsimprint=SPFs
        for i in range(m):
             SPFsimprint[0,i,:]=SPFs[0,i,:]*np.exp(phase*1j)

        RST['node'+ str(int(node))] = SPFsimprint
        #Build Wfn
        wpack = QDTK.Wfn(tape=tuple(newTape.astype(np.int64)))

        ind = 0
        psi = np.zeros(0)
        for nd in wpack.tree._swapDown:
            ind = ind+1
            psi = np.append(psi,RST['node'+ str(ind)].flatten())
        wpack.PSI = psi
        wpack.createWfnFile(FileOut)   


	print "\t{x} saved".format(x=FileOut)

####	END Small Helper Routines
########################################################################

########################################################################																####
####	Tools 		##
		
def Check(IN,default):
	if IN=='':
		return default
	else:
		return IN


####	END Tools       ##
########################################################################	

########################################################################
########################################################################
####		##
####	MAIN 	##

usage= """ This Program does some small helper tasks """
parser=OptionParser(usage=usage)

parser.add_option('-i','--in', dest='IN', type='str', default='',
                  help='Usage: -i FileInName -> gives the filename of a special Fortran file. This option works only, if ONE transformation is choosen.')
parser.add_option('-o','--out', dest='OUT', type='str', default='',
                  help='Usage: -o FileOutName -> saves the output .mat file as FileOutName.mat. If this option is not choosen, the output file is named after the input file. This option works only, if ONE transformation is choosen.')                  
parser.add_option('--cutpsi', dest='DO_CUTPSI', action='store_true', default=False,
                  help='Cuts the Fortran psi file from T_0 to T and creates a restart file at T. Needed: paraList[0]=T; Optional: paraList[1]=T_0')
parser.add_option('--phaseimprint', dest='DO_PHASE_IMPRINT', action='store_true', default=False,
                  help='Imprints a spatial dependent phase onto the SPFs of a restart file. Needed: paraList[0]=node, stringList[0]=hamiltFile, stringList[1]=imprintfunction, paraList[1:]=imprintfunctionparameters')
parser.add_option('-p','--parameter', action='append', dest='paraList', type='float', default=[],
                    help='Add parameter values to a list; You can call -p over and over.')
parser.add_option('-s','--string', action='append', dest='stringList', type='string', default=[],
                    help='Add strings to a list; You can call -s over and over.')
options, args = parser.parse_args(sys.argv[1:])

print "\nRunning SmallHelper.py"
print "================================================================"
print "\t\t\t Program in TEST!!!!!!"
print "================================================================"

DoneSOMETHING = False
	
if options.DO_CUTPSI:
	FileIn = Check(options.IN,"psi")
	FileOut= Check(options.OUT,"psi_cut")
        if len(options.paraList) != 1 and len(options.paraList) != 2:
           raise ValueError('In DO_CUTPSI: T(-p T) not found')
        if len(options.paraList) == 1:
           T = options.paraList[0]
	   CUTPSI(FileIn,FileOut,T)
        if len(options.paraList) == 2:
           T = options.paraList[0]
           T0 = options.paraList[1]
           CUTPSI(FileIn,FileOut,T,T0)
	DoneSOMETHING = True
if options.DO_PHASE_IMPRINT:
        import QDTK
	FileIn = Check(options.IN,"restart")
	FileOut= Check(options.OUT,"restart_imprint")
        FileHamilt = "hamilt"
        FileHamilt = options.stringList[0]
        func = options.stringList[1]
        node = options.paraList[0]
        funcPar = options.paraList[1:]
	PHASE_IMPRINT(FileIn,FileHamilt,FileOut,node,func,funcPar)
	DoneSOMETHING = True

if DoneSOMETHING==False:
	print "\tNothing done. Please check something :-)"

####                    ##
####	END MAIN        ##	
########################################################################
########################################################################


															####

