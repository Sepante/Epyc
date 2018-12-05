from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

input_file_address = "network data/clean/"
input_file_name = "clean primaryschool.txt"
input_file =  input_file_address + input_file_name 
output_file_address = "network data/giant/"
#input_file_name = "clean email.txt"
#input_file_name = "clean FilmForum.txt"
#input_file_name = "clean FilmMessages.txt"



pandas_data = pd.read_csv( input_file , sep ='\t', header = None)

raw_data = np.array( pandas_data[[0,1,2]] ) #for the case in which we have 2 extra columns of data.
data = raw_data.copy()

vertices_num = np.max( data[:, 1:] ) + 1

G = nx.Graph()
for edge in data:
    G.add_edge( edge[1], edge[2] )

comps = (sorted(nx.connected_components(G), key = len, reverse=True))
comp_size = np.zeros(len (comps), dtype = int )

for i in range( len(comps) ):
    comp_size[i] = len(comps[i])


print ( Counter(comp_size) )
    
giant_component = comps[ comp_size.argmax() ]
#"""
for vertex in range( vertices_num + 1 ):
    if vertex not in giant_component:
        data = data [np.all([data[:,2] != vertex, data[:,1] != vertex],axis = 0)]
        print (vertex)
#"""
#"""
nav_list = set(data[:,1]) | set(data[:,2])
nav_list = sorted(list(nav_list))
for i in nav_list:
    print(i)
    data[data[:,2]==i ,2] = nav_list.index(i)
    data[data[:,1]==i ,1] = nav_list.index(i)

pd_output = pd.DataFrame(data)
output_file_name = output_file_address + "giant " + input_file_name
output_file_info = output_file_address + "info giant " + input_file_name
content = pd_output.to_csv( output_file_name, header = None , index = None , sep = '\t' )

edge_average = len(data) / (data[-1, 0] - data[0, 0])
vertices_num = np.max( data[:, 1:] ) + 1
with open(output_file_info, 'w') as f:
    f.write("vertices:\t" + str(vertices_num) + '\n')
    f.write("edge average:\t" + str(edge_average))
#"""