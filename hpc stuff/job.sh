#!/bin/bash -l
#PBS -N sis_two_dis
##PBS -l mem=160MB
#PBS -l nodes=1:ppn=12
#PBS -l walltime=10:00:00
cd /home/samhz.physics.sharif/SIS/run
./a.out
