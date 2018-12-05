import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import importlib as im
import networkReader
im.reload(networkReader)
from networkReader import *

#for undirected graphs

shuffleType = "DCB"
output_file_address = "../network data/shuffled/" + shuffleType +"/"


pandas_data = pd.read_csv( input_file , sep ='\t', header = None)

raw_data = np.array( pandas_data[[0,1,2]] ) #for the case in which we have 2 extra columns of data.
data = raw_data.copy()

vertices_num = np.max( data[:, 1:] ) + 1
edges = raw_data[:, 1:].copy()
##if undirected:
invertedEdges = edges[:,1] < edges[:,0] #we want to treat the graph as undirected, so we keep
                                        #vertices with smaller number, to the left.
edges[invertedEdges, 0] , edges[invertedEdges, 1] = edges[invertedEdges, 1] , edges[invertedEdges, 0]

eventList = [list(edge) for edge in edges]
edgeSet = {tuple(edge) for edge in edges} #just a temporary container for 
                                        #finding unique edges.
edgeList = [list(edge) for edge in edgeSet] #contains all edges. (not the events)
                                            #since every edge has multiple events

## singleLinkEvent is a list of lists, which stores every time-stamp an edge had
## an event (has appeared). it corresponds to the edges stored in the edgeList.
singleLinkEvent = [ [] for edge in edgeList ]
for i , event in enumerate(eventList):
    singleLinkEvent[ edgeList.index(event) ].append( i )
    #adds timesatmps of each edge, to the respecting list, in the
    #singleLinkEvent list.
    if i%1000 == 0:
        print(i)

np.random.shuffle(singleLinkEvent)

for i, eventSeries in enumerate(singleLinkEvent):
    edges [ eventSeries ] = edgeList[ i ] #puts every edge in the new
                                        #timestamps, it has aquired.
    if i%100 == 0:
        print(i)
                                        

data[:, 1:] = edges

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
