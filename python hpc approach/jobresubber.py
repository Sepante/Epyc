#!/usr/bin/env python
import csv, subprocess
import numpy as np
from string import digits

with open('qstat.txt') as f:
    qstat_text = f.readlines()

#qsub_command = "qstat -i"
#print(qsub_command)
#qstat_text = subprocess.check_output(qsub_command, shell = True)
#print(exit_status.stdout)
#result = subprocess.check_output(['ls', '-l'])

#result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
#result.stdout.decode('utf-8')
#print("AND NOW:")
#print(exit_status)



qstat_text = qstat_text[0]
qstat_text = qstat_text.split('\\n')
qstat_text = qstat_text[5:-1]

i = 0
for i in range( len(qstat_text) ):
    job_id, job_state = qstat_text[i].split('.hpc.ce.sh')
    job_state = job_state.strip('- ')
    _, job_p_value = job_state.split('brazil-')
    job_p_value = job_p_value.split(' ')[0]
    
    print(job_state[-1])
    print(job_p_value)
    print(job_id)
