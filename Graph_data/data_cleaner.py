import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from collections import Counter

#lines = open('tij_InVS.dat').read().splitlines()
input_file_address = "network data/original/"
output_file_address = "network data/clean/"
input_file_name = "primaryschool.txt"
#input_file_name = "sociopattern_hospital.dat"
#input_file_name = "sociopattern_hospital.txt"

input_file =  input_file_address + input_file_name 
pandas_data = pd.read_csv( input_file , sep =',', header = None)

raw_data = np.array( pandas_data[[0,1,2]] ) #for the case in which we have 2 extra columns of data.
#raw_data = np.array(pandas_data)
data = raw_data.copy()

##WARNING!!
#switching time and edge columns, if necessary
#data[:,2] , data[:,0] = data[:,0] , data[:,2].copy()
#"""
#adjusting the node labels in order to work with smaller numbers (as node labels).
nav_list = set(data[:,1]) | set(data[:,2])
nav_list = sorted(list(nav_list))
for i in nav_list:
    print(i)
    data[data[:,2]==i ,2] = nav_list.index(i)
    data[data[:,1]==i ,1] = nav_list.index(i)

#"""
vertices_num = np.max( data[:, 1:3 ].ravel() ) + 1
#data starts from zero
data[:,0] -= data[0,0]

#time_check (to see if the time data has been considerd correctly
#and not confused with an edge list, by checking if data is increasing)
if np.sum(data[:-1, 0] > data[1:, 0] ):
    print("ALERT!!!!")
else:
    print("time? check!")

#this data has a very big gap, this line fixes deletes the gap.
#data[60623:,0] -= 54920
#data[100:,0] += 100

#this data is short we double it's period by repeating the edges
#data[len(lines):] = data[:len(lines)]
#jump = data[len(lines),0] - data[len(lines)-1,0]
#data[len(lines):,0]+=(-jump + 20)
"""

#"""
pd_output = pd.DataFrame(data)
output_file_name = output_file_address + "clean " + input_file_name
output_file_info = output_file_address + "info " + input_file_name
content = pd_output.to_csv( output_file_name, header = None , index = None , sep = '\t' )
#content = pd_output.to_csv( None , header = None , index = None , sep = '\t' )
#"""
"""
with open(output_file_name, 'w') as f:
    #content = f.read()
    f.seek(0, 0)
    f.write("vertices: \t" + str(vertices_num) + '\n' + content )
"""
edge_average = len(data) / (data[-1, 0] - data[0, 0])

with open(output_file_info, 'w') as f:
    f.write("vertices:\t" + str(vertices_num) + '\n')
    f.write("edge average:\t" + str(edge_average))
#q = np.diff(data[:,0])

#non_zeros_ind = q != 0

#q = q[non_zeros_ind]
#print(min(q))
