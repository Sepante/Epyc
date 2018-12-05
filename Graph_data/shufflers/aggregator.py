import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import importlib as im
import networkReader
im.reload(networkReader)
from networkReader import *

#for undirected graphs

shuffleType = "agg"
output_file_address = "../network data/" + shuffleType +"/"

edges = raw_data[:, 1:].copy()

G = nx.Graph()

for edge in edges:
    G.add_edge( np.min(edge), np.max(edge) )
    #print(edge)
    

edgeArray = np.array(G.edges())
edgeArray.sort(1)


sortKey = np.argsort(edgeArray[:,0])
edgeArray = edgeArray[sortKey]


#data[:, 1:] = edges

pd_output = pd.DataFrame(edgeArray)

output_file_name = shuffleType + ' ' + input_file_name

output_file = output_file_address + output_file_name
output_file_info = output_file_address + "info " + output_file_name
content = pd_output.to_csv( output_file, header = None , index = None , sep = '\t' )
#"""
#edge_average = len(data) / (data[-1, 0] - data[0, 0])
vertices_num = np.max( data[:, 1:] ) + 1
with open(output_file_info, 'w') as f:
    f.write("vertices:\t" + str(vertices_num) + '\n')
    #f.write("edge average:\t" + str(edge_average))
#"""