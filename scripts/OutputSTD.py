#!/usr/bin/env python

"""
OutputSTD
=========
:Abstract:
	The file contains functions which read in the fortran output files and transform them to .mat files. So they can be easy implemented in matlab and python.

:Authors:
	- V. Bolsinger vbolsing@physnet.uni-hamburg.de (VB)
        - J. Schurer   jschurer@physnet.uni-hamburg.de (JS)

:Version:
	0.0 of 27.09.2013
	
:Status:
	To be tested

:Content:
	- ReadENO(FileName,FileOut) by VB (Tested)
	- ReadGDEN(FileName,FileOut) by VB (Tested for 1D systems and 3D systems)
	- ReadGPOP(FileName,FileOut) by VB (To be tested)
	- ReadRED2B(FileName,FileOut) by JS (To be tested)
	- ReadPSI(FileName,FileOut) by JS (To be tested)
	- ReadNORB(FileName,FileOut) by VB (To be tested)
	- ReadCOEF(FileName,FileOut) by VB (To be tested)
	- ReadDECH(FileName) by VB (To be tested)
	- ReadNPOP(FileName,FileOut) by VB (To be tested)
	- ReadFIXB(FileName,FileOut) by JS (To be tested)
	- ReadExpect(FileName,FileOut) by JS (To be tested)
	- ReadMomDis(FileName,FileOut) by JS (To be tested)
	- ReadOPER(FileName) by VB (To be tested)
        - ReadEVAL(FileName) by JS (To be tested)
        - ReadEVEC_SPF(FileName) by JS (To be tested)
	- ReadDmatSPF(FileName) by VB (To be tested)
	- ReadDmat2SPF(FileName) by JS (To be tested)
        - ReadEVEC_GRID(FileName) by VB (To be tested)

:History:
	- 27.09.2013 VB wrote the function ReadENO.
	- 07.10.2013 VB finished writing the functions ReadGDEN and ReadGPOP
	- 09.10.2013 VB wrote the functions for ReadPSI and  ReadNORB
	- 10.10.2013 VB included ReadCOEF and the parsing stuff
	- 11.10.2013 VB finished the functions ReadDECH and ReadNPOP
	- 17.10.2013 JS rewriting of ReadPSI to have data sorted correctly
	- 23.10.2013 JS Red2B read in added
	- 11.12.2013 JS Read Fixed Basis output
	- 13.01.2014 JS ReadExpect added
	- 29.04.2014 JS ReadMomDis added
	general remark: In higher dimensions, the delimitor for a new block 
	changes from \n to emptySpace\n. An additional condition is needed
	to identify new blocks of data: if line[0:1] == "\n" or len(line)==2
	- 19.05.2014 VB Extend gden, ReadRED2B to three dimensions.
	- 28.05.2014 VB added ReadOPER
	- 11.07.2014 VB include the new style created by dmat and dmat2
	- 30.08.2014 JS & VB correction of norb routine (last time step was not saved) 
    - 20.10.2014 JS Change of ReadPSI for Multi-species
    - 18.11.2014 JS Add of ReadEVAL for the read in of dmat and dmat2 eigenvalues
    - 01.12.2014 JS Add of ReadEVEC_SPF to get geminals 
    - 13.03.2015 VB ReadDmatSPF is added
    - 27.03.2015 VB fixed bug for 3D natpops.
    - 28.04.2015 JS Correct ReadEVAC to work for Multispecies
    - 20.05.2015 VB IndentationError:
    - 26.05.2015 JS Bug correction in ReadEVEC_SPF: ready for multispecies
    - 01.06.2015 JS Add of ReadDmat2SPF
    - 04.09.2015 VS Add of ReadEVEC_GRID, which is the same as ReadNORB!

		
:License:	
	
:Notes:
	- Done: psi-, output-, gpop-, gden, norb, natpop, coefdist
	- To do: format in files -> print "{0:10.4f}".format(x)
	- The functions can be extended, so more errors that may occur can be handeled
	- use help(Header) in python to get these informations
	
"""

import scipy.io as scIo
from numpy import reshape, array
from optparse import OptionParser
import sys
from warnings import  filterwarnings
from math import sqrt
filterwarnings("ignore", category=FutureWarning) 

########################################################################
####						ReadENO 								####
########################################################################
def ReadENO(FileName, FileOut):
	""" Reads in the fortran file 'output' (time, norm, energy, orthogonality) and saves it as .mat files"""
	
	t = [] # time
	E = [] # Energy
	n = [] # Norm
	O = [] # Ortogonality
	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')
	for line in fin:
		i,j,k,l = line.split()
		t.append(float(i))
		E.append(float(k))
		n.append(float(j))
		O.append(float(l))
	fin.close()

	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict={'time': t, 'energy': E, 'norm': n,'overlap': O})
	print "\t{x}.mat saved".format(x=FileOut)


########################################################################
####						ReadExp 								####
########################################################################
def ReadExpect(FileName, FileOut):
	""" Reads in the fortran file 'expect' (<x>) and saves it as .mat files"""
	
	t = [] # time
	x = [] # op_exp
	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')
	for line in fin:
		i,j,k = line.split()
		t.append(float(i))
		x.append(complex(float(j),float(k)))
	fin.close()

	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict={'time': t, 'op_exp': x})
	print "\t{x}.mat saved".format(x=FileOut)


########################################################################
####						ReadGDEN								####
########################################################################
def ReadGDEN(FileName,FileOut):
	""" Reads in the fortran file 'gpop' and saves it as .mat files.
		
	The working method is as followed: Line by line the file is readed. If the line startes with #, then the time is saved, if there is an empty line, this is an hint that in the next line a new data block starts. If a new data block starts, the old datas are saved in a list, and then cleared for the new datas. If there is a new degree of freedom, than an new list is created. """

	t = []          #time
	L_dof = []      #List of the degrees of freedom
	DOF = 0         #actual degree of freedom
	newData = True  #Is only true, when a new block (time step) of data is read
	bool = True

	debug=False

	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')

	with open(FileName) as fp:
		for line in fp:
			if line == "\n" or line == " \n" or line=="  \n": #go to next line and start a new block
				#sadly in two different styles the gden is saved, differs on the dimension!
				if debug: print "\tNew Block found"
				newData = True
				continue
			elif line[0:1].strip()=="#": #Catch the time
				t.append(float(line[1:line.find("[")].strip()))
				continue

			List = line.split()			
			
			if newData:
				if debug: print "\tHandle data Block"
				newData = False
				if DOF != 0: #Save the old values, but NOT in the first case
					M = reshape(data,(GridSize,GridSize))
					exec("Value{j}.append(M)".format(j=DOF))
					exec("if Grid{j}==[]:Grid{j}=x".format(j=DOF)) 
				else: #Do one time at the beginning
					GridSize = int(float(List[1]))  #second entry gives the number of grid points
													#First entry is the DOF

				if not List[0] in L_dof: #If this DOF is not in the list L_dof then it is included
					if debug: print "\tInclude DOF in list"
					L_dof.append(List[0])
					exec("Value{j}=[]".format(j=int(float(List[0]))))
					exec("Grid{j}=[]".format(j=int(float(List[0]))))
				
				
				DOF = List[0] #Set the actual degree of freedom and delet the old variables
				data = []    #clear the variable for the new values
				x = []        #clear the grid points for the new dof
				k = 0		  #Counter for the grid points, so that only the first grid points are saved.
				continue
				
			if len(List) == 4: #Save the datas for gden	
				data.append(complex(float(List[2]),float(List[3])))
				if k < GridSize: #save the grid
					x.append(float(List[1]))
					k=k+1
					continue
	#print data
 	M = reshape(data,(GridSize,GridSize))
 	exec("Value{j}.append(M)".format(j=DOF))
	fp.close()	


	Dic = {'time': t}
	Dic['dof1']= Value1
	for i in L_dof:
		exec( "Dic['dof{i}']=Value{i}".format(i=i))
		exec( "Dic['grid"+i+"']= Grid"+i)
	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=Dic)
	print "\t{x}.mat saved.".format(x=FileOut)


########################################################################
####						ReadRED2B								####
########################################################################
def ReadRED2B(FileName,FileOut):
	""" Reads in the fortran file 'red2b' and saves it as .mat files.
		
	The working method is as followed: Line by line the file is readed. If the line startes with #, then the time is saved, if there is an empty line, this is an hint that in the next line a new data block starts. If a new data block starts, the old datas are saved in a list, and then cleared for the new datas. If there is a new degree of freedom, than an new list is created. """

	t = []          #time
	L_dof = []      #List of the degrees of freedom
	DOF = 0         #actual degree of freedom
	newData = True  #Is only true, when a new block (time step) of data is read
	bool = True
	
	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')

	with open(FileName) as fp:
		for line in fp:
			if line == "\n" or line==" \n" or line=="  \n": #go to next line and start a new block
				#sadly in two different styles the gden is saved, differs on the dimension!
				newData = True
				continue
			elif line[0:1].strip()=="#": #Catch the time
				t.append(float(line[1:line.find("[")].strip()))
				continue

			List = line.split()			

			if newData:
				newData = False
				if DOF != 0: #Save the old values, but NOT in the first case
					M = reshape(data,(GridSize,GridSize))
					exec("Value{j}.append(M)".format(j=DOF))
					exec("if Grid{j}==[]:Grid{j}=x".format(j=DOF)) 
				else: #Do one time at the beginning
					GridSize = int(float(List[2]))

				if not List[0] in L_dof: #If this DOF is not in the list L_dof then it is included
					L_dof.append(List[0])
					exec("Value{j}=[]".format(j=int(float(List[0]))))
					exec("Grid{j}=[]".format(j=int(float(List[0]))))
								
				DOF = List[0] #Set the actual degree of freedom and delet the old variables
				data = []    #clear the variable for the new values
				x = []        #clear the grid points for the new dof
				k = 0		  #Counter for the grid points, so that only the first grid points are saved.
				continue
				
			if len(List) == 3: #Save the datas for red2b				
				data.append(float(List[2]))
				if k < GridSize: #save the grid
					x.append(float(List[1]))
					k=k+1
					continue
	M = reshape(data,(GridSize,GridSize))	#Save Last data set
 	exec("Value{j}.append(M)".format(j=DOF))
	fp.close()	


	Dic = {'time': t}
	Dic['dof1']= Value1
	for i in L_dof:
		exec( "Dic['dof{i}']=Value{i}".format(i=i))
		exec( "Dic['grid"+i+"']= Grid"+i)
	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=Dic)
	print "\t{x}.mat saved.".format(x=FileOut)

########################################################################
####						ReadGPOP								####
########################################################################
def ReadGPOP(FileName,FileOut):
	""" Reads in the fortran file 'gpop' and saves it as .mat files.
	The working method is nearly the same as in ReadGDEN, and is explained there."""
	
	
	t = []          #time
	L_dof = []      #List of the degrees of freedom
	DOF = 0         #actual degree of freedom
	newData = True  #Is only true, when a new block of data is read
	
	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')

	with open(FileName) as fp:
		for line in fp:
			List = line.split()
			
			if List == []: #go to next line and start a new block
				newData = True
				continue
			elif List[0]=="#": #Catch the time
				t.append(float(List[1]))
				newData = True
				continue

			if newData:
				newData = False
				LengthOfGrid = List[1]
				if DOF != 0: #Save the old values, but NOT in the first case
					exec("value{j}.append(data)".format(j=DOF))
					exec("Grid{j}=x".format(j=DOF))
				else: #Do one time at the beginning
					GridSize = int(float(List[1]))
				
				if not List[0] in L_dof: #If this DOF is not in the list L_dof then it is included
					L_dof.append(List[0])
					exec("value{j}=[]".format(j=int(float(List[0]))))
					exec("Grid{j}=[]".format(j=int(float(List[0]))))
								
				DOF = int(float(List[0])) #Set the actual degree of freedom and delet the old variables
				data = []    #clear the variable for the new values
				x = []        #clear the grid points for the new dof
				k = 0		  #Counter for the grid points, so that only the first grid points are saved.
				continue

			if len(List) == 2 : #Save the datasfor gpop
				data.append(complex(float(List[1])))
				if k<LengthOfGrid: #save the grid
					x.append(float(List[0]))
					k=k+1
					continue
	
	exec("value{j}.append(data)".format(j=DOF))
	exec("Grid{j}=x".format(j=DOF))
			
	fp.close()
	Dic = {'time': t}
	for i in L_dof:
		 exec( "Dic['dof"+i+"']= value"+i)
		 exec( "Dic['grid"+i+"']= Grid"+i)
	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=Dic)
	print "\t{x}.mat saved".format(x=FileOut)


########################################################################
####						ReadPSI 								####
########################################################################
def ReadPSI(FileName, FileOut):
	"""Reads in the fortran file 'psi' and saves it as .mat files.
	
	The working method: The routine runs line by line through the program and saves the data for all times into <psi> of structure [time][node][spf][coefficients].  This data is then saved per node{j} with structure [time][spf][coefficients]."""

	comment = "Syntax: node{i}:[time][spf][coefficients] ; time:[time]"
	time = []		# Array for the times
	psi  = []       # List for the psi data
	tape = []    	# List for tape data
    
	tree = QDTK.Node.Node() # Tree object for the iteration over the nodes

	try: IN = open(FileName,'r') # Check if all file exists and  open
	except: raise ValueError(FileName +' not found')
	for ll in IN:
		
		if ll.strip()=='$tape':  # Tape is created
			temp = ''
			ll = IN.next()
			while not (ll == '\n' or ll ==" \n"):	 # Collect tape data
				temp = temp + ',' + ll.strip()
				ll = IN.next()
			for i in temp[1:].split(','): tape.append(int(i)) #Append to tape list
			tree.init_from_tape(tape)	#Create Tree object
			tree._createLevelOrder()
			
		if ll.strip()=='$time': # Find new Time
			ll = IN.next()
			time.append(float(ll.strip().split()[0]))
			
		if ll.strip()=='$psi':  # Parse coefficient section
			psiT = []
			for nd in tree._topNode._swapLvlOrder: # Iterate over all Nodes
				func = []
				temp = ''
				comp = 0j
				for i in range(0,nd._phiTot):  # Iterate over all coefs of one Node
					temp = IN.next().replace('(', '').replace(')','').strip().replace(' ','').split(',')
					comp = complex(float(temp[0]),float(temp[1]))
					func.append(comp)
				h = array(func) # Create Array to store all coeff of one Node in Matrix format (#SPFs)x(#SubSPFs)
				psiT.append(h.reshape(nd._dim,nd._phiLen).tolist())  # write into psi of one time
			psi.append(psiT)	# append to psi for all times
	IN.close() 
    
    #Reorder for saveing
	for nd in tree._topNode._swapLvlOrder:
		exec("node{j}=[]".format(j=nd._nodeNum))	# Initialized node lists
	for t in psi:
		ind = 0
		for nd in tree._topNode._swapLvlOrder:
                        nodeT = t[ind]
                        ind = ind+1
                        exec("node{j}.append({nodeT})".format(j=nd._nodeNum,nodeT=nodeT))	# Append data of one time to node{j}

    ### Write into .mat file
	Dic = {'comment': comment, 'time': time, 'tape': map(float,tape)}
	for nd in tree._topNode._swapLvlOrder:
		exec( "Dic['node{j}']=node{j}".format(j=nd._nodeNum))
		
	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=Dic)
	print "\t{x}.mat saved".format(x=FileOut)





# Commented by jschurer due to replacement by new Routine

#def ReadPSI(FileName,FileOut):
	#"""Reads in the fortran file 'psi' and saves it as .mat files.
	
	#The working method: The routine runs line by line through the program and saves the data into a helping variable <H>. if a new psi function starts, the old datas are saved intpo <psi>"""
	
	#t = []                #time
	#WriteTime = False     #This boolean is needed, because the time is marked as $time, but the value of the times stands in the next line.
	#WritePsi  = False      #same as for WriteTime
	#psi = []
	#H = []
	
	#try: fin = open(FileName, 'r+')
	#except: raise ValueError(FileName +' not found')
		
	#with open(FileName) as f:
		#for line in f:
			#if line[0:1] == "\n":
				#continue
			#if line[0:5]=="$time":
				#WriteTime = True
				#continue
			#if WriteTime==True:
				#t.append(float(line[1:line.find("[")].strip()))
				#WriteTime = False
				#continue
			#if line[0:4]=="$psi":
				##Save old datas
				#if H != []:
					#psi.append(H)
					#H = []

				#WritePsi = True
				#continue
			#if WritePsi == True:
				#line = line.replace("("," ")
				#line = line.replace(")"," ")
				#line = line.replace(","," ")
				#List = line.split()
				#Real = float("{0:4.3f}".format(float(List[0])))
				#Imag = float("{0:4.3f}".format(float(List[1])))
				#H.append(complex(Real,Imag))
	#psi.append(H)	
	#f.close()
	
	#Dic = {'time': t, 'psi':psi}
	#scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=Dic)
	#print "\t{x}.mat saved".format(x=FileOut)
	


########################################################################
####						ReadNORB 								####
########################################################################
def ReadNORB(FileName,FileOut):
	"""Reads in the fortran file 'norb' and saves it as .mat files.
	
	Working method: The routine runs line by line through the norb file and saves the values of every column into helping variables. If the time changes, these helping variables are saved and cleared for the next data block."""

	t = [0]  #time
	x = []   #grid
	GridSaved = False #If true, the grid willNOT be saved anymore
	DoAtBegin = True  #Do only at the beginning
	
	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')
		
	with open(FileName) as f:
		for line in f:
			LINE = line.split()
			
			if DoAtBegin: #do only at the beginning
				DOF = (len(LINE)-2)/2  #Number of DOF
				for j in range(1,DOF+1):
					exec("dof{j}=[]".format(j=j))
					exec("H{j}=[]".format(j=j))   #H is a helping-variable
				DoAtBegin = False
			
			if float(LINE[0]) > t[-1]:   #new time step
				t.append(float(LINE[0])) #save time
				if GridSaved==False:     #Check if grid is already saved
					GridSaved=True
				for j in range(1,DOF+1): #Save helping variables
					exec("dof{j}.append(H{j})".format(j=j))
					exec("H{j}=[]".format(j=j))
			
			if GridSaved==False:    
				x.append(float(LINE[1]))
			for j in range(1,DOF+1):
				Real = float(LINE[2*j])
				Imag = float(LINE[2*j+1])
				exec("H{j}.append(complex(Real,Imag))".format(j=j))
			
	f.close()
	
	#Save data of last time step
	for j in range(1,DOF+1): #Save helping variables
		exec("dof{j}.append(H{j})".format(j=j))

	Dic = {'time': t, 'grid': x}
	for j in range(1,DOF+1):
		 exec( "Dic['dof{j}']= dof{j}".format(j=j))
	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=Dic)
	print "\t{x}.mat saved".format(x=FileOut)


########################################################################
####						ReadFIXB 								####
########################################################################
def ReadFIXB(FileName,FileOut):
	"""Reads in the fortran analysis file 'fixB' and saves it as .mat files.
	
	Working method: The routine runs line by line through the norb file and saves the values of every column into helping variables. If the time changes, these helping variables are saved and cleared for the next data block."""

	t = []  #time
	Cn= []
	DoAtBegin = True  #Do only at the beginning
	
	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')
		
	with open(FileName) as f:
		for line in f:
			LINE = line.split()
			
			if DoAtBegin: #do only at the beginning
				NN = ((len(LINE)-1)/3)  #Number of Numberstates
				DoAtBegin = False

			
			t.append(float(LINE[0]))
			
			CnT = []
			for j in range(1,NN+1):
				Real = float(LINE[j].strip())
				Imag = float(LINE[NN+j].strip())
				CnT.append(complex(Real,Imag))
			
			Cn.append(CnT)
			
	f.close()
		
	Dic = {'time': t,'Cn':Cn}

	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=Dic)
	print "\t{x}.mat saved".format(x=FileOut)

########################################################################
####						ReadCOEF								####
########################################################################
def ReadCOEF(FileName,FileOut):
	"""Reads in the fortran file 'coef' and saves it as .mat files.
	
	Working method is the same as ReadNORB.
	"""
	t = [0]  #time
	v = []   #value
	DoAtBegin = True  #Do only at the beginning
	
	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')
		
	with open(FileName) as f: #----------------------------------begin-1
		for line in f:
			LINE = line.split()
			
			if DoAtBegin: #do only at the beginning---------------------
				if len(LINE[1])==1: #Check out which type of file is COEF
					node ="bosonic"
					K=0  #find the first rwo with the coefficients
					for k in LINE[1:]:
						if len(k)==1:
							K=K+1 #first column of data
						else:
							fc = K
				else:
					node="normal"
					fc = 2  #first column of data
			
				DOF = (len(LINE)-fc)/2  #Find number of DOF-------------
				for j in range(1,DOF+1): #Initial variables-------------
					exec("spf{j}=[]".format(j=j))
					exec("H{j}=[]".format(j=j))   #H is a helping-variable
					value=[]
				DoAtBegin = False
			
			if float(LINE[0]) > t[-1]:   #new time step-----------------
				t.append(float(LINE[0])) #save time
				for j in range(1,DOF+1): #Save helping variables--------
					exec("spf{j}.append(H{j})".format(j=j))
					exec("H{j}=[]".format(j=j))
				value.append(v)
				v=[]
			
			v.append(float(LINE[1])) #Read data from file---------------
			for j in range(0,DOF):
				Real = float(LINE[fc+2*j])
				Imag = float(LINE[fc+2*j+1])
				exec("H{j}.append(complex(Real,Imag))".format(j=j+1))
			
	f.close() #----------------------------------------------------end-1
		
	Dic = {'time': t, 'coef': value}
	for j in range(1,DOF+1):
		 exec( "Dic['spf{j}']= spf{j}".format(j=j))
	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=Dic)
	print "\t{x}.mat saved".format(x=FileOut)

########################################################################
####						ReadDECH								####
########################################################################
def ReadDECH(FileName):
	""" Reads in both <write_psi_chiffre> and <write_psi_chiffre2>."""

	debug=False
	
	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')
	
	inde = []  #index
	laye = [0] #Layer of coefficient
	node = [1] #number of node
	ndpa = [1] #node number with respect to parent node 
	tynd = ''  #string with the type of  the node
	spfn = [1] #number of the spf
	conf = []  #configuration
	coef = []  #coefficients for the first timestep
	been = [1]
	BEEN = []
	
	with open(FileName) as f2: Lines = f2.readlines() #-----------------
	f2.close()
	
	if len(Lines[17].split()[5]) != 1: tf=2   #Filetype with coefficients. Created by write_psi_chiffre2
	else: tf=0  							  #Filetype without coefficients. Created by write_psi_chiffre
	
	for LINE in Lines: #------------------------------------------------		
		if LINE[0]=="#": continue
		if LINE[0]=="\n":continue
		
		data = LINE.split()
		
		if node[0] < int(float(data[2])): #New node, save data----------
			been.append(int(float(data[0]))-1)
			BEEN.append(been)
			been = [int(float(data[0]))]
			
			
			NODE = {'index':inde, 'layer':laye, 'node':node,'type':tynd, 'coef':coef, 'spf':spfn, 'config':conf, 'nodeParent':ndpa, 'BeginEndIndex':BEEN}
			exec"scIo.savemat('node{i}.mat',  mdict=NODE)".format(i=node[0])
			if debug: print "\tnode{i}.mat saved".format(i=node[0])
			
			node[0] = int(float(data[2]))
			inde = []
			coef = []
			conf = []
			spfn = [1]
			BEEN = []		
					
		inde.append(int(float(data[0])))
		
		if data[1] > laye[0]: laye[0] = int(float(data[1]))
		
		if data[3] != ndpa[0] : ndpa[0] = int(float(data[3]))
		
		if data[4]!=tynd:
			if   data[4]=='1' :tynd= 'bosonic'
			elif data[4]=='0' :tynd="normal"
			elif data[4]=='2' :tynd="primitive"
			elif data[4]=='-1':tynd="fermionic"
			else: print "Error in ReadDECH: #0001"
		
		if tf==2:
			real = float(data[5])
			imag = float(data[6])
			coef.append(complex(real,imag))
			
		ActSpf=int(float(data[5+tf]))	
		if ActSpf > spfn[-1]:
			spfn.append(ActSpf)
			been.append(int(float(data[0]))-1)
			BEEN.append(been)
			been = [int(float(data[0]))]
			conf = []
			
			
		
		h = []
		for i in range(6+tf,len(data)):
			 h.append(int(float(data[i]))-1)
		conf.append(h)
			
	been.append(int(float(data[0])))
	BEEN.append(been)
	NODE = {'index':inde, 'layer':laye, 'node':node,'type':tynd, 'coef':coef, 'spf':spfn, 'config':conf, 'nodeParent':ndpa, 'BeginEndIndex':BEEN}
	exec("scIo.savemat('node{i}.mat',  mdict=NODE)".format(i=node[0])) #
	print "\tnode{i}.mat saved".format(i=node[0])


########################################################################
####						ReadNPOP								####
########################################################################
def ReadNPOP(FileName,FileOut):
	"""Reads in the fortran file 'natpop' and saves it as .mat files.
	
	Working method: First, the functions reads in all the lines in the file and 'delet' not importatnt informations. Then it goes backwards and add linebraks to the next line. """
	
	t = []     #time
	VALUE=[]   #Values [M0, M1, M2,...] for different times, with M1=[m1,m2,...]
			   #different nodes and m1=[1000, 0.000, ....]
	M = []     #Saves the npop values of a special grid
	Store = "" #Stores the line if the next line isn't a new node
	DoAtBegin = True

	Lines = [] #Read in file in an nice way-----------------------------
	with open(FileName) as f: 
		for line in f:
			if line[0] == "\n" :continue
                        if line[1] == "\n" :continue
			if line[0:8]==' Natural': continue
			if line[0:5]==' node': continue
			else: Lines.append(line[1:-1])		
	f.close()
		
	for i in range(len(Lines)-1,-1,-1): #reads in Lines backwards-------
		if Lines[i][0]==' ':
			Store = Store + Lines[i]
			continue
		if Lines[i][0]=='m':
			LINE = Lines[i][3:]+Store
			Store = ""
			lll = []
			for j in LINE.split(): lll.append(float(j))
			M.insert(0,lll)
			continue
		if Lines[i][0:5].strip()=="time:":
			t.insert(0,float(Lines[i][6:Lines[i].find("[")].strip()))
			L = len(M)
			if DoAtBegin:
				for k in range(0,L):
					exec("node{k}=[]".format(k=k+1))
				DoAtBegin = False
			for k in range(0,L):
				exec("node{K}.insert(0,M[{k}])".format(K=k+1, k=k))
			M=[]
	
	DIC = {'time':t}#---------------------------------------------------
	for k in range(1,L+1):
		exec("DIC['node{k}']=node{k}".format(k=k))
	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=DIC)
	print "\t{x}.mat saved".format(x=FileOut)

		
########################################################################
####						readin_grid								####
########################################################################
def readin_grid(foper,dof=1):
    """ read in DVR weights for dof from file foper """
    tag_w = '$weight_'+str(dof)
    tag_x = '$grid_'+str(dof)
    j   = 0 # j=0:not found, j=1: tag_x found -> line = #gridpounts, j=2 actual gridpoints, j=3 done
    i   = 0 # i=0:not found, i=1: tag_w found -> line = #gridpounts, i=2 actual weights, i=3 done
    IN  = open(foper,'r')
    for line in IN:
        if line.strip()==tag_x:
            j=1
            continue
        if line.strip()==tag_w:
            i=1
            continue
        if j==1:
            j=j+1
            continue
        if j==2:
            x = line.split()
            j=3
            continue
        if i==1:
            i=i+1
            continue
        if i==2:
            w = line.split()
            i=3
            continue
    IN.close()
    x = np.array(x,'float')
    w = np.array(w,'float')

    return x,w 


########################################################################
####						ReadMomDis								####
########################################################################
def ReadMomDis(FileIn,FileOut):
	"""Reads in the fortran file 'mom_distr_1' and saves it as .mat files. WORKS ONLY FOR 1D AND ONE NODE"""
	
	t = []     # time
	grid = []  # Grid
	distr = [] # Helper
	distrT= [] # Momentum distribution 
	try: fin = open(FileIn, 'r+')
	except: raise ValueError(FileIn +' not found')

	countT=0;
        i,j,k = fin.readline().split()
        t.append(float(i))
	grid.append(float(j))
        distr.append(float(k))
	for line in fin:
		i,j,k = line.split()
                if float(i) == t[countT]:
	             grid.append(float(j))
                     distr.append(float(k))
                else:
                     countT=countT+1
		     t.append(float(i))
                     grid = []
                     grid.append(float(j))
                     distrT.append(distr)
                     distr = []
                     distr.append(float(k))
	fin.close()
        distrT.append(distr)

	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict={'time': t, 'grid': grid, 'mom_distr': distrT})
	print "\t{x}.mat saved".format(x=FileOut)


########################################################################
####						ReadOPER								####
########################################################################
def ReadOPER(FileName,FileOut):
	""" Reads in the text file 'Operator' and saves it as .mat files. """

	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')
	dof =1
	grid = []
	weight =[]

	with open(FileName) as fp:
		for line in fp:
			if line == "$bosonic_degfs\n":
				nextline = fp.next()
				dofMax=int(nextline.split()[0])
				continue
			
			if eval('line == "$grid_{dof}\\n"'.format(dof=dof)):
				nextline = fp.next()
				n =int(nextline.split()[0])
				nextline = fp.next()
				x=[]
				for i in range(n):
					x.append(float(nextline.split()[i]))
				grid.append(x)
				continue
				
			if eval('line == "$weight_{dof}\\n"'.format(dof=dof)):
				nextline = fp.next()
				n =int(nextline.split()[0])
				nextline = fp.next()
				w=[]
				for i in range(n):
					w.append(float(nextline.split()[i]))
				weight.append(w)
				
				if dof+1 > dofMax:
					break
				else:
					dof=dof+1
					continue

                                
	fp.close()	


	Dic = {'grid': grid, 'weight':weight}
	#Dic['dof1']= Value1
	#for i in L_dof:
		#exec( "Dic['dof{i}']=Value{i}".format(i=i))
		#exec( "Dic['grid"+i+"']= Grid"+i)
	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict=Dic)
	print "\t{x}.mat saved.".format(x=FileOut)


########################################################################
####						ReadEVAL								####
########################################################################
def ReadEVAL(FileName, FileOut):
	""" Reads in the fortran file 'eval_dmat(2)_dofX_dofY' and saves it as .mat files"""
	
	t = [] # time
	occ = [] # occupations numbers
	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')
	for line in fin:
		LINE = line.split()
		t.append(float(LINE[0]))
		temp = []
                for j in range(1,len(LINE)):
			temp.append(float(LINE[j]))
		occ.append(temp)
	fin.close()

	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict={'time': t, 'eval': occ})
	print "\t{x}.mat saved".format(x=FileOut)


########################################################################
####						ReadEVEC_SPF								####
########################################################################
def ReadEVEC_SPF(FileName, FileOut):
	""" Reads in the fortran file 'evec_dmat(2)_dofX_dofY_spf' and saves it as .mat files"""
	
	t = [] # time
	evec = [] # occupations numbers
	
	evec_temp = [] #single eigenvector
	evecs_temp = [] # all eigenvectors a time t

	firstT = True
	firstX = True
	dim1 = 0
        dim2 = 0

	try: fin = open(FileName, 'r+')
	except: raise ValueError(FileName +' not found')
	for line in fin:
		if line[0:1].strip()=="#": #Catch the time
			t.append(float(line[1:line.find("[")].strip()))
			if firstT:
				firstT = False
			else:
				M = reshape(evec_temp,(dim1,dim2))
				evecs_temp.append(M)
				evec_temp = []
				evec.append(evecs_temp)
				evecs_temp = []
				firstX = True
			continue

		LINE = line.split()

		if len(LINE) == 2 or len(LINE) == 3:
			if firstX:
				dim1 = int(LINE[1])
				if len(LINE) == 3:
                                    dim2 = int(LINE[2])
                                else:
                                    dim2 = int(LINE[1])
				firstX = False
			else:
				M = reshape(evec_temp,(dim1,dim2))
				evecs_temp.append(M)
				evec_temp = []
			continue

		if len(LINE) == 4:
			evec_temp.append(complex(float(LINE[2]),float(LINE[3])))
			continue
	
	M = reshape(evec_temp,(dim1,dim2))
	evecs_temp.append(M)
	evec.append(evecs_temp)
	fin.close()

	scIo.savemat('{x}.mat'.format(x=FileOut),  mdict={'time': t, 'evec': evec})
	print "\t{x}.mat saved".format(x=FileOut)



########################################################################
####						ReadDmatSPF								####
########################################################################
def ReadDmatSPF(FileName, FileOut):
    """ Reads in the fortran file dmat_ndX_spf and saves it as .mat files"""
    
    t      = [] # time
    M      = [] # matrix, where dmat is stored
    Mtemp  = [] # matrix temporal
    
    time0  = 0  # initial time
    counter= 0  # counter
    DoOnce = True
    
    try: fin = open(FileName, 'r+')
    except: raise ValueError(FileName +' not found')
    
    for line in fin:
        time,idx1,idx2,realPart,imagPart = line.split()
        time = float(time)
        idx1 = int(idx1)
        idx2 = int(idx2)
        realPart = float(realPart)
        imagPart = float(imagPart)
        
        if DoOnce == True:
            time0  = time
            DoOnce = False
        if (time == time0):
            counter = counter+1
            Mtemp.append(realPart + 1j*imagPart)
        elif(time > time0):
            t.append(time0) #Add onld time
            time0 = time
            
            n = int(sqrt(counter))
            M.append(array(Mtemp).reshape(n,n))
            Mtemp = []
            
            #for this line
            counter = 1  
            Mtemp.append(float(realPart) + 1j*float(imagPart))
            
        else:
            print 'ERROR'
            
    fin.close()
    t.append(time0) #Add onld time
    n = int(sqrt(counter))
    M.append(array(Mtemp).reshape(n,n))
    
    scIo.savemat('{x}.mat'.format(x=FileOut),  mdict={'time': t, 'dmatSPF': M})
    print "\t{x}.mat saved".format(x=FileOut)

########################################################################
####						ReadDmat2SPF								####
########################################################################
def ReadDmat2SPF(FileName, FileOut):
    """ Reads in the fortran file dmat2_ndX_spf and saves it as .mat files"""
    
    t      = [] # time
    M      = [] # matrix, where dmat is stored
    Mtemp  = [] # matrix temporal
    
    time0  = 0  # initial time
    counter= 0  # counter
    DoOnce = True
    
    try: fin = open(FileName, 'r+')
    except: raise ValueError(FileName +' not found')
    
    for line in fin:
        time,idx1,idx2,idx3,idx4,realPart,imagPart = line.split()
        time = float(time)

        realPart = float(realPart)
        imagPart = float(imagPart)
        
        if DoOnce == True:
            time0  = time
            DoOnce = False
        if (time == time0):
            counter = counter+1
            Mtemp.append(realPart + 1j*imagPart)
        elif(time > time0):
            t.append(time0) #Add onld time
            time0 = time
            print counter
            n = int(sqrt(sqrt(counter)))
            M.append(array(Mtemp).reshape(idx1_old,idx2_old,idx3_old,idx4_old))
            Mtemp = []
            
            #for this line
            counter = 1  
            Mtemp.append(float(realPart) + 1j*float(imagPart))
            
        else:
            print 'ERROR'
        
        idx1_old = int(idx1)
        idx2_old = int(idx2)
        idx3_old = int(idx3)
        idx4_old = int(idx4)    
    fin.close()
    t.append(time0) #Add onld time
    n = int(sqrt(sqrt(counter)))
    M.append(array(Mtemp).reshape(idx1_old,idx2_old,idx3_old,idx4_old))
    
    scIo.savemat('{x}.mat'.format(x=FileOut),  mdict={'time': t, 'dmat2SPF': M})
    print "\t{x}.mat saved".format(x=FileOut)


########################################################################
########################################################################
####																####
####						Tools 									####
####																####
########################################################################
########################################################################
			
def Check(IN,STRING):
	if IN=='':
		return STRING
	else:
		return IN

			
########################################################################
########################################################################
####																####
####						MAIN 									####
####																####
########################################################################
########################################################################
usage= """The program reads in the fortran output files and transform them to .mat files. So they can be easy implemented in matlab and python. """
parser=OptionParser(usage=usage)

parser.add_option('-i','--in', dest='IN', type='str', default='',
                  help='Usage: -i FileInName -> gives the filename of a special Fortran file. This option works only, if ONE transformation is choosen.')
parser.add_option('-o','--out', dest='OUT', type='str', default='',
                  help='Usage: -o FileOutName -> saves the output .mat file as FileOutName.mat. If this option is not choosen, the output file is named after the input file. This option works only, if ONE transformation is choosen.')                  
parser.add_option('--output', dest='DO_OUTPUT', action='store_true', default=False,
                  help='Transforms the Fortran output file')
parser.add_option('--expect', dest='DO_EXPECT', action='store_true', default=False,
                  help='Transforms the Fortran expect file')
parser.add_option('--dmat', dest='DO_GDEN', action='store_true', default=False,
                  help='Transforms the Fortran one body density matrix into matlab file')
parser.add_option('--gden', dest='DO_GDEN', action='store_true', default=False,
                  help='Transforms the Fortran gden file (same as dmat)')
parser.add_option('--dmat2', dest='DO_RED2B', action='store_true', default=False,
                  help='Transforms the Fortran two body reduced density matrix into matlab file')
parser.add_option('--red2b', dest='DO_RED2B', action='store_true', default=False,
                  help='Transforms the Fortran red2b file (same es dmat2)')
parser.add_option('--gpop', dest='DO_GPOP', action='store_true', default=False,
                  help='Transforms the Fortran gpop file')
parser.add_option('--psi', dest='DO_PSI', action='store_true', default=False,
                  help='Transforms the Fortran psi file')
parser.add_option('--norb', dest='DO_NORB', action='store_true', default=False,
                  help='Transforms the Fortran norb file') 
parser.add_option('--coef', dest='DO_COEF', action='store_true', default=False,
                  help='Transforms the Fortran coef file')   
parser.add_option('--fixb', dest='DO_FIXB', action='store_true', default=False,
                  help='Transforms the fixed basis analysis file')   
parser.add_option('--momDis', dest='DO_MOMDIS', action='store_true', default=False,
                  help='Transforms the momentum distribution file. WORKS ONLY FOR 1D AND ONE NODE')   
parser.add_option('--npop', dest='DO_POP', action='store_true', default=False,
                  help='Transforms the Fortran natpop file. (Node numbering can be incorrect !!)')   
parser.add_option('--dech', dest='DO_DECH', action='store_true', default=False,
                  help='Transforms the file created by QDTK/Wavefunction/write_psi_chiffre into a .mat file. Both styles write_psi_chiffre and write_psi_chiffre2 can be handeled. The output is node1.mat, node2.mat... and cant be changed.')
parser.add_option('--oper', dest='DO_OPER', action='store_true', default=False,
                  help='Transforms the Operator file created by python into a .mat file.')         
parser.add_option('--eval', dest='DO_EVAL', action='store_true', default=False,
                  help='Transforms the eigenvalues of dmat and dmat2 file created by python into a .mat file.')      
parser.add_option('--evec_spf', dest='DO_EVEC_SPF', action='store_true', default=False,
                  help='Transforms the eigenvectors of dmat and dmat2 file created by python into a .mat file, with respect to a spf representation.')      
parser.add_option('--evec_grid', dest='DO_EVEC_GRID', action='store_true', default=False,
                  help='Transforms the eigenvecors of dmat and dmat2 file created by python into a .mat file. This is the same as --norb. The first line containes the time. No structured output required.')      
parser.add_option('--dmatSPF', dest='DO_DMATSPF', action='store_true', default=False,
                  help='Transforms the file  dmat_nd2_spf created by qdtk_analysis.x ... -dmat -nd X -spfrep -diagonalize into a .mat file.')   
parser.add_option('--dmat2SPF', dest='DO_DMAT2SPF', action='store_true', default=False,
                  help='Transforms the file  dmat2_nd2_spf created by qdtk_analysis.x ... -dmat2 -nd X -spfrep -diagonalize into a .mat file.')   
options, args = parser.parse_args(sys.argv[1:])
options, args = parser.parse_args(sys.argv[1:])


print "\nRunning OutPutSTD.py"
print "================================================================"
print "\t\t\t Program in TEST!!!!!!"
print "(Be carefull with: node indices, multi species)"
print "================================================================"

DoneSOMETHING = False
if options.DO_OUTPUT:
	FileIn = Check(options.IN,"output")
	FileOut= Check(options.OUT,FileIn)
	ReadENO(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_EXPECT:
	FileIn = Check(options.IN,"expect")
	FileOut= Check(options.OUT,FileIn)
	ReadExpect(FileIn,FileOut)
	DoneSOMETHING = True
	
if options.DO_GDEN:
	FileIn = Check(options.IN,"gden")
	FileOut= Check(options.OUT,FileIn)
	ReadGDEN(FileIn,FileOut)
	DoneSOMETHING = True
	
if options.DO_GPOP:
	FileIn = Check(options.IN,"gpop")
	FileOut= Check(options.OUT,FileIn)
	ReadGPOP(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_RED2B:
	FileIn = Check(options.IN,"red2b")
	FileOut= Check(options.OUT,FileIn)
	ReadRED2B(FileIn,FileOut)
	DoneSOMETHING = True


	
if options.DO_PSI:
	import QDTK
	FileIn = Check(options.IN,"psi")
	FileOut= Check(options.OUT,FileIn)
	ReadPSI(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_FIXB:
	FileIn = Check(options.IN,"fixb")
	FileOut= Check(options.OUT,FileIn)
	ReadFIXB(FileIn,FileOut)
	DoneSOMETHING = True
	
if options.DO_NORB:
	FileIn = Check(options.IN,"norb")
	FileOut= Check(options.OUT,FileIn)
	ReadNORB(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_COEF:
	FileIn = Check(options.IN,"coef_of_nd_1")
	FileOut= Check(options.OUT,FileIn)
	ReadNORB(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_DECH:
	FileIn = Check(options.IN,"psi_chiffre")
	if options.OUT != "":
		print "No output options is allowed with --dech"
		exit()
	ReadDECH(FileIn)
	DoneSOMETHING = True
	
if options.DO_POP:
	FileIn = Check(options.IN,"natpop")
	FileOut= Check(options.OUT,FileIn)
	ReadNPOP(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_MOMDIS:
	FileIn = Check(options.IN,"mom_distr_1")
	FileOut= Check(options.OUT,FileIn)
	ReadMomDis(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_OPER:
	FileIn = Check(options.IN,"Hamilt")
	FileOut= Check(options.OUT,FileIn)
	ReadOPER(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_EVAL:
	FileIn = Check(options.IN,"eval_dmat2_dof1_dof1")
	FileOut= Check(options.OUT,FileIn)
	ReadEVAL(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_DMATSPF:
	FileIn = Check(options.IN,"dmat_nd2_spf")
	FileOut= Check(options.OUT,FileIn)
	ReadDmatSPF(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_DMAT2SPF:
	FileIn = Check(options.IN,"dmat2_nd2_spf")
	FileOut= Check(options.OUT,FileIn)
	ReadDmat2SPF(FileIn,FileOut)
	DoneSOMETHING = True

if options.DO_EVEC_SPF:
	FileIn = Check(options.IN,"evec_dmat2_dof1_dof1_spf")
	FileOut= Check(options.OUT,FileIn)
	ReadEVEC_SPF(FileIn,FileOut)
	DoneSOMETHING = True
        
if options.DO_EVEC_GRID:
	FileIn = Check(options.IN,"evec_dmat2_dof1_dof1_grid")
	FileOut= Check(options.OUT,FileIn)
	ReadNORB(FileIn,FileOut)
	DoneSOMETHING = True

if DoneSOMETHING==False:
	print "\tNothing done. Please check something :-)"

#ReadGDEN("Tests_OutPutStandard/gden_npo100_dof2")
#ReadGPOP("Tests_OutPutStandard/gpop_npo18_dof3")
#ReadGPOP("Test/gpopSven","Test")
#ReadPSI("psi")
#ReadNORB('norb_1')
#ReadCOEF("Tests_OutPutStandard/coef_of_nd_1","Test")
#ReadDECH("Test/psi_chiffre")
#ReadNPOP("Tests_OutPutStandard/natpop","Test")
