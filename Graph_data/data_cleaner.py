import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from collections import Counter

#lines = open('tij_InVS.dat').read().splitlines()
lines = open('primaryschool.csv').read().splitlines()
#data = np.zeros( (len(lines), 3) ,int)
data = np.zeros( (2*len(lines), 3) ,int)
for i in range (len(lines)):
    #data[i] = (lines[i].split(','))
    data[i] = (lines[i].split(','))    
nav_list = set(data[:,1]) | set(data[:,2])

nav_list = sorted(list(nav_list))

"""data starts from zero"""
data[:,0] -= data[0,0]


output = open('clean_input_matrix.txt', 'w')

""" this data has a very big gap, this line fixes deletes the gap."""
data[60623:,0] -= 54920
#data[100:,0] += 100

""" this data is short we double it's period by repeating the edges."""
data[len(lines):] = data[:len(lines)]
jump = data[len(lines),0] - data[len(lines)-1,0]
data[len(lines):,0]+=(-jump + 20)



for line in data:
   output.write( str(line[0]) + '\t' + str(nav_list.index(line[1])) + '\t' + str(nav_list.index(line[2])) + '\n' )
output.close()

q = np.diff(data[:,0])

non_zeros_ind = q != 0

q = q[non_zeros_ind]
print(min(q))
