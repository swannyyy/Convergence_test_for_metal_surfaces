# Convergence_test_for_metal_surfaces
This script will eventually allow to run in an automated way all the initial convergence tests for a metal surface investigation in VASP. Such tests are K points and ENCUT convergence, as well as the surface energy vs. layer thickness evaluated through a modified Fiorentini-Methfessel method 

Every change must be notified through a comment inside the code as well as any idea for new implementation.

## How to get things set to work with git
Since we are going to code a script that it is meant to work on a HCP platform (katana in our case) it will be more effective and simple to directly code on katana avoiding jupyter notebook except for very simple tests that do not need neither VASP nor PBS.
So after you access katana go in a diractory that will contain the directory where you will code and type:

    git clone https://github.com/swannyyy/Convergence_test_for_metal_surfaces NameDir

Where NameDir is the name of a new directory that will be created that will contain all the shared files.
Now go inside this new directory and type: (THIS PASSAGE IS PROBABLY UNNECESSARY) 

    git init

It is pretty important at this point to set both your name and email in your local git directory using:
    
    git config --global user.name "Friedrich Nietzsche"  
    git config --global user.email f.nietzsche@ubermensch.de

Since you are not a dead german philosopher put your name and email instead :)

Now your directory is fully set to work with the shared one in the cloud.
Before updating the shared directory in the cloud you must be sure that your code is working since others will work on the same code afterwards, and fixing others bugs is difficult and annoying.
If you are not sure of the validity of your code just put it into a new branch through this command:

    git checkout -b <branch-name>
In this way you will be working on a separate branch and you will be able to play with the code as much as you want without impacting it.

Once you are sure of the modification you have made and you have tested them you can apply the changes to the main file executing the following commands:

    git pull
    git commit 
    git push -a 
    
## How to work with ASE package on katana 
First of all ASE is not a standard package so you won't find it preinstalled on katana, this means that you will need to install it if you want to perform tests and eventually run the script.
In order to istall it you will need to execute the following command no matter where in katana:

    pip install --upgrade --user ase

After you got the package installed you will need to modify some enviromental variable so that VASP can be executed inside the python environment.
Open then the .bashrc file and add the following lines just after the export PATH line:
  
    export PYTHONPATH=/.local/bin/ase:$PYTHONPATH
    export PATH=/.local/bin/ase:$PATH
    export ASE_VASP_COMMAND="qsub VASP_vtst.pbs"
    export VASP_PP_PATH=/srv/scratch/YOUR_zID/PBEpotentials_VASP
    export SYS_VASP=system

