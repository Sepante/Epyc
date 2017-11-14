import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

lines = open('tij_InVS.dat').read().splitlines()
data = np.zeros( (len(lines), 3) ,int)
for i in range (len(lines)):
    data[i] = (lines[i].split())    
nav_list = set(data[:,1]) | set(data[:,2])

nav_list = sorted(list(nav_list))

output = open('clean_input_matrix.txt', 'w')

for line in data:
   output.write( str(line[0]) + '\t' + str(nav_list.index(line[1])) + '\t' + str(nav_list.index(line[2])) + '\n' )
output.close()

q = np.diff(data[:,0])

non_zeros_ind = q != 0

q = q[non_zeros_ind]

