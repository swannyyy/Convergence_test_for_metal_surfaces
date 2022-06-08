# Convergence_test_for_metal_surfaces
This script will eventually allow to run in an automated way all the initial convergence tests for a metal surface investigation in VASP. Such tests are K points and ENCUT convergence, as well as the surface energy vs. layer thickness evaluated through a modified Fiorentini-Methfessel method 

Every change must be notified through a comment inside the code as well as any idea for new implementation.

## How to get things set to work with git
Since we are going to code a script that it is meant to work on a HCP platform (katana in our case) it will be more effective and simple to directly code on katana avoiding jupyter notebook except for very simple tests that do not need neither VASP nor PBS.
So after you access katana go in a diractory that will contain the directory where you will code and type:

    git clone https://github.com/swannyyy/Convergence_test_for_metal_surfaces NameDir

Where NameDir is the name of a new directory that will be created that will contain all the shared files.
Now go inside this new directory and type:

    git init

Now your directory is fully set to work with the shared one in the cloud.
Before updating the shared directory in the cloud you must be sure that your code is working since others will work on the same code afterwards, and fixing others bugs is difficult and annoying.
If you are not sure of the validity of your code just put it into a new branch through this command:

    git checkout -b <branch-name>
In this way you will be working on a separate branch and you will be able to play with the code as much as you want without impacting it.

Once you are sure of the modification you have made and you have tested them you can apply the changes to the main file executing the following commands:

    git pull
    git commit 
    git push -a 


