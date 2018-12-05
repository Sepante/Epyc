import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from collections import Counter

#lines = open('tij_InVS.dat').read().splitlines()
input_file_address = "network data/clean/"
output_file_address = "network data/normal/"
input_file_name = "clean sociopattern_conference_contact.txt"
#input_file_name = "clean sociopattern_hospital.txt"
#input_file_name = "clean brazil.txt"

input_file =  input_file_address + input_file_name 
pandas_data = pd.read_csv( input_file , sep ='\t', header = None)

raw_data = np.array( pandas_data[[0,1,2]] ) #for the case in which we have 2 extra columns of data.
#raw_data = np.array(pandas_data)
data = raw_data.copy()

data[:,0] = np.round(data[:, 0] /240)
#"""
pd_output = pd.DataFrame(data)
output_file_name = output_file_address + "normal " + input_file_name
output_file_info = output_file_address + "info " + input_file_name
pd_output.to_csv( output_file_name, header = None , index = None , sep = '\t' )
#content = pd_output.to_csv( None , header = None , index = None , sep = '\t' )
#"""
#"""
def Burst(i_t_times):
    return ( np.std(i_t_times) - np.mean(i_t_times) ) / (np.std(i_t_times) + np.mean(i_t_times) )


edge_average = len(data) / (data[-1, 0] - data[0, 0])
vertices_num = np.max( data[:, 1:3 ].ravel() ) + 1
with open(output_file_info, 'w') as f:
    #content = f.read()
    f.seek(0, 0)
    f.write("vertices: \t" + str(vertices_num) + '\n')
    f.write("edge average:\t" + str(edge_average) + '\n' )
    f.write("burst:\t" + str(Burst ( np.diff(data[:, 0]) ) ))
#"""

print("burst:\t" + str(Burst ( np.diff(data[:, 0]) ) ))
print("edge average:\t" + str(edge_average) + '\n' )
