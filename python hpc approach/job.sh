#!/bin/bash -l
#PBS -l nodes=1:ppn=1
#PBS -m abe
#pbs -M sinasajjadi@protonmail.com
#PBS -q LSPR
cd /home/seyedebrahim.saj.physics.sharif/network/Src
./run <<< "${p} ${r} ${runNum}"
