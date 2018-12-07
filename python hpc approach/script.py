#!/usr/bin/env python
import csv, subprocess
import numpy as np

parameter_file_full_path = "prange.csv"

fromFile = False
if ( fromFile ):
    with open(parameter_file_full_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for job in reader:
            qsub_command = "qsub -v p={0},runNum={1} job.sh".format(*job)
    
            #print qsub_command # Uncomment this line when testing to view the qsub command
    
            # Comment the following 3 lines when testing to prevent jobs from being submitted
            exit_status = subprocess.call(qsub_command, shell=True)
            #if exit_status is 1:  # Check to make sure the job submitted
                #print "Job {0} failed to submit".format(qsub_command)
    #print "Done submitting jobs!"
else:
    prange = np.arange(0.1025, 0.1275,0.0025)
    r = 0.0001
    runNum = 1000
    jobNumber = 20
    for p in prange:
        for i in range(jobNumber):
            job = [ str(p), str(r), str(runNum) ]
            qsub_command = "qsub -v p={0},r={1},runNum={2} brazil-{0} job.sh".format(*job)
            print(qsub_command)
            exit_status = subprocess.call(qsub_command, shell=True)
