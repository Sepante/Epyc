import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import importlib as im
import networkReader
im.reload(networkReader)
from networkReader import *

#for undirected graphs

shuffleType = "SOU"
output_file_address = "../network data/shuffled/" + shuffleType +"/"


edges = raw_data[:, 1:].copy()
##if undirected:
invertedEdges = edges[:,1] < edges[:,0] #we want to treat the graph as undirected, so we keep
                                        #vertices with smaller number, to the left.
edges[invertedEdges, 0] , edges[invertedEdges, 1] = edges[invertedEdges, 1] , edges[invertedEdges, 0]

time_stamps = data[:,0]

time_stamps = np.random.randint( time_stamps.min(), time_stamps.max(), len( data ) )
time_stamps.sort()

data[:,0] = time_stamps

#"""
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
#"""