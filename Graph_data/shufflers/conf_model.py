from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import importlib as im
import networkReader
im.reload(networkReader)
from networkReader import *

#for undirected graphs
shuffleType = "D"
output_file_address = "../network data/shuffled/" + shuffleType +"/"




pandas_data = pd.read_csv( input_file , sep ='\t', header = None)

raw_data = np.array( pandas_data[[0,1,2]] ) #for the case in which we have 2 extra columns of data.
data = raw_data.copy()

vertices_num = np.max( data[:, 1:] ) + 1

deg_sequence = np.zeros( vertices_num, dtype = int )

#G = nx.MultiGraph()
for i, edge in enumerate(data):
    deg_sequence[ edge[1] ] += 1
    deg_sequence[ edge[2] ] += 1
    #G.add_edge( edge[1], edge[2] )
    #if (i%100000 == 0):
        #print(i)

print("done with reading the graph")
Q = nx.configuration_model( deg_sequence )

edges = np.array(Q.edges)[:, :2] #networkx stores the edges of a multigraph
                                #in triplets, the third value being another
                                #indice to distinguish same edges.
                                #we reject that value.
np.random.shuffle(edges)        #and then shuffle all edges.

data[:, 1:] = edges





comps = (sorted(nx.connected_components(Q), key = len, reverse=True))
#comps = (sorted(nx.connected_components(G), key = len, reverse=True))
comp_size = np.zeros(len (comps), dtype = int )

for i in range( len(comps) ):
    comp_size[i] = len(comps[i])

networkIsConnected = True
if (comp_size[0] != vertices_num):
    print( "network not connected!" )
    networkIsConnected = False
else:
    print( "network -> connected!" )
    networkIsConnected = True
    
if( not networkIsConnected ):
    print("trying to find carve out the giant component")
    
    giant_component = comps[ comp_size.argmax() ]
    #"""
    for vertex in range( vertices_num + 1 ):
        if vertex not in giant_component:
            data = data [np.all([data[:,2] != vertex, data[:,1] != vertex],axis = 0)]
            #print (vertex)
    #"""
    #"""
    nav_list = set(data[:,1]) | set(data[:,2])
    nav_list = sorted(list(nav_list))
    for i in nav_list:
        if(i % 100 == 0):
            print(i)
        data[data[:,2]==i ,2] = nav_list.index(i)
        data[data[:,1]==i ,1] = nav_list.index(i)
    
    
pd_output = pd.DataFrame(data)
output_file_name = shuffleType + "-sh " + input_file_name
output_file = output_file_address + output_file_name
output_file_info = output_file_address + "info " + output_file_name
content = pd_output.to_csv( output_file, header = None , index = None , sep = '\t' )

edge_average = len(data) / (data[-1, 0] - data[0, 0])
vertices_num = np.max( data[:, 1:] ) + 1
with open(output_file_info, 'w') as f:
    f.write("vertices:\t" + str(vertices_num) + '\n')
    f.write("edge average:\t" + str(edge_average))
