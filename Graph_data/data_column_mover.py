import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from collections import Counter


#input_file_address = "network data/giant/"
input_file_address = "network data/shuffled/DCB/"
#output_file_address = "network data/clean/"
output_file_address = "./"
#input_file_name = "primaryschool.txt"
#input_file_name = "sociopattern_hospital.dat"
input_file_name = "DCB-sh clean sociopattern_hospital.txt"

input_file =  input_file_address + input_file_name 
pandas_data = pd.read_csv( input_file , sep ='\t', header = None)

raw_data = np.array( pandas_data[[0,1,2]] ) #for the case in which we have 2 extra columns of data.
#raw_data = np.array(pandas_data)
data = raw_data.copy()

data[:,2] , data[:,0] = data[:,0] , data[:,2].copy()

pd_output = pd.DataFrame(data)
output_file_name = output_file_address + "column-sw " + input_file_name

content = pd_output.to_csv( output_file_name, header = None , index = None , sep = ' ' )
#content = pd_output.to_csv( None , header = None , index = None , sep = '\t' )
#"""
"""
with open(output_file_name, 'w') as f:
    #content = f.read()
    f.seek(0, 0)
    f.write("vertices: \t" + str(vertices_num) + '\n' + content )
"""
edge_average = len(data) / (data[-1, 0] - data[0, 0])

