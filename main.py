#!/usr/bin/env python
# coding: utf-8





from ase import Atoms
from ase.calculators.vasp import Vasp
import subprocess
from ase.build import hcp0001, fcc111, add_adsorbate, bulk,surface
from ase.io import write
from ase.io.vasp import write_vasp
import os
import shutil
import time

#The following function defines all the parameters for the geometry optimisation of a bulk metal
# In[ ]:
def bulkopt(system):
	calculator = Vasp(istart=0,
                icharg=2,
                iniwav=1,
                nelm=150,
                nelmin=6,
                algo='Fast',
                ispin =2,
                ediff=1e-05,
                ismear=-5,
                sigma=0.2,
                prec='Accurate',
                encut=eCut,
                xc='PBE',
                ncore=4,
                lwave =False,
                lcharg =False,
                laechg =False,
                lreal=False,
                nedos=1200,
                lorbit=11,
                ediffg=-0.05,
                ibrion=2,
                isif=3,
                nsw=300,
                potim=0.2,
                ivdw=12,
                kpts=(k1,k2,k3),
                gamma=True)
	system.calc = calculator
	try:
		system.get_total_energy()
	except:
		print()
#The following function defines all the parameters for the optimisation of a slab
def slabopt(system):
	try:
		calculator = Vasp(istart=0,
			icharg=2,
			iniwav=1,
			nelm=150,
			nelmin=6,
			algo='Fast',
			ispin =2,
			ediff=1e-05,
			ismear=-5,
			sigma=0.2,
			prec='Accurate',
			encut=eCut,
			xc='PBE',
			ncore=4,
			lwave =False,
			lcharg =False,
			laechg =False,
			lreal=False,       
			nedos=1200,
			lorbit=11,
			ldipol=True,
			idipol=3,
			ediffg=-0.05,
			ibrion=2,
			isif=1,
			nsw=300,
			potim=0.2,
			ivdw=12,
			kpts=(k1,k2,k3),
			gamma=True)
		system.calc = calculator
		system.get_total_energy()
	except:
		print('ERROR: Calculation running correctly only in: ',vasp_dir,'Check the calculation settings in the script please!')
# In[3]:

#This function has been adapted from a script to freez the atoms below a certain cutoff and shift all the atoms at the bottom of the cell since they are put in the center as default by ase.
def freezeatoms(cutoff):
    import sys
    import os
    import string

    # column = [0, 1, 2, 3, 4, 7]
    # Properties = ['RMSD', 'TA', 'BF', 'CE', 'ASA', 'HBB']
    i = 0
#    Vacuum_space=15.0
    inputFilename = 'POSCAR'
    output = ''
    energyListCounter = 0

    # cutoff=sys.argv[1]
    print(cutoff)
    dirName = 'FrozenAtoms_{}'.format(cutoff)

    listAtoms = []
    isDispl = {}
  
    inputfile = open(inputFilename, 'r')  # Open POSCAR file and read it
    input = inputfile.readlines()
    inputfile.close
    lineCtr = 0
    systemNrOfAtoms = 0
    for line in input:
        
        lineCtr = lineCtr + 1
        if lineCtr == 7:  # Read the seventh line which contains the number of each atom in the system
            tmpLine = line.split()
            for ctr in range(0, len(tmpLine)):
                systemNrOfAtoms = systemNrOfAtoms + int(tmpLine[ctr])  # Calculate the total number of atoms in the system
        if lineCtr == 8:
            output = output + 'Selective Dynamics\n'  # Add the keyword "Selective dynamics" to the POSCAR file used for optimization
            
        if lineCtr > 8 and lineCtr < 9 + systemNrOfAtoms:
            atomNr = lineCtr - 8
            f = line.split()
            if float(f[2]) > float(cutoff):
                f[2]=float(f[2])-(Vacuum_space)
                #print(f[2])
                linea = line.split()[0] + " " + line.split()[1] + " " +str((float(line.split()[2])-(Vacuum_space))) +' T T T\n'
                output= output + linea
            else:
                f[2]=float(f[2])-(Vacuum_space)
#               print(line.split())
                #print(f)
                #output = (line.split())[0]+ (line.split()[1] +(line.split())[2] + (line.split('\n'))[0] + ' F F F\n'
                linea = line.split()[0] + " " + line.split()[1] + " " +str((float(line.split()[2])-(Vacuum_space))) +' F F F\n'
                output= output + linea
                listAtoms.append(lineCtr - 8)
        else:
            if lineCtr < 9:  # Print all the lines before the "Selective dynamics" keyword as they were in the POSCAR input file
                output = output + line
        listAtomsSorted = sorted(listAtoms)  # Sort the numbers labeling the atoms that are being displaced
        
#    os.makedirs(dirName)
#    outputfilename = dirName + '/POSCAR'
    outputfilename ='POSCAR'
    outputfile = open(outputfilename, 'w')  # Write the POSCAR file for frequency calculations in the folder that has been generated
    outputfile.write(output)
    outputfile.close()
#
#START OF THE GEOMETRY BUILDING PART
#

if not os.path.exists('Ru_bulk'): #check if the directory for the bulk calc has already been created
        os.makedirs('Ru_bulk')    #create directory
shutil.copy('VASP_vtst.pbs', 'Ru_bulk/')
os.chdir('Ru_bulk')

#ENCUT AND KPOINTS ARE SET MANUALLY BUT THEY WILL BE READ FROM ENCUT AND KPOINT TESTS CODED BY XIAO SA
eCut=400
k1=12
k2=12
k3=7


bulk_name= 'POSCAR'
metal_bulk = bulk ('Ru','hcp',a=2.68102,b=4.24926) #this command creates the geometry and saves it in a variable
write_vasp(bulk_name, metal_bulk)     #write the POSCAR file 
bulkopt(metal_bulk)                   #launch optimisation


#CURRENTLY WE HAVE NO WAY TO CHECK IF THE CALC HAS FINISHED OR NOT SO THE PBS CHECK CODED BY AZZY SHOULD STAY HERE 
#time.sleep(180)   #three minutes is pretty enough for this calc to finish but a proper check on the job would be better



#analyse the final geometry and saves the geometrical parameters in a set of variables further used to build the slab
cell_mat=metal_bulk.get_cell()
a_vec=cell_mat[0]
b_vec=cell_mat[1]
c_vec=cell_mat[2]
a_optBulk=a_vec[0]
b_optBulk=b_vec[1]
c_optBulk=c_vec[2]
#print(c_optBulk)
os.chdir('../')
#
#SLABS CREATION FOR SURFACE ENERGY CONVERGENCE 
#
limit =[3,4]
eCut=400
k1=2
k2=2
k3=1
Vacuum_space=15.0
index = limit[0]
e_slab=[]
while index<= limit[1]:

    
    slab = hcp0001('Ru', size=(1, 2, index),a=a_optBulk, c=c_optBulk, vacuum=Vacuum_space, orthogonal=True)
    slab.pbc=True
    vasp_dir= '{}L'.format(index)
    if not os.path.exists(vasp_dir):
        os.makedirs(vasp_dir)
    slab_name= 'POSCAR'.format(index)
    slab_nameOrig= '{}L.vasp'.format(index)
    shutil.copy('VASP_vtst.pbs', vasp_dir)
    
    os.chdir(vasp_dir)
    
    write_vasp(slab_name, slab)
    write_vasp(slab_nameOrig, slab)
    cutoff=18

    
    slabopt(slab)
    freezeatoms(cutoff)


    os.chdir('../')
    e_slab.append(slab.get_total_energy())
    print(e_slab)
    index=index+1  


# e_slab = slab.get_total_energy()
#
# print('Potential energy:', e_slab )

# In[ ]:





