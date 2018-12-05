import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import importlib as im
import networkReader
im.reload(networkReader)
from networkReader import *

#for undirected graphs

shuffleType = "DCWB"
output_file_address = "../network data/shuffled/" + shuffleType +"/"

edges = raw_data[:, 1:].copy()
##if undirected:
invertedEdges = edges[:,1] < edges[:,0]
edges[invertedEdges, 0] , edges[invertedEdges, 1] = edges[invertedEdges, 1] , edges[invertedEdges, 0]

eventList = [list(edge) for edge in edges]
edgeSet = {tuple(edge) for edge in edges}
edgeList = [list(edge) for edge in edgeSet]
#edgeEventList = 

singleLinkEventList = [ [] for edge in edgeSet ]
for i , event in enumerate(eventList):
    #print(i, edge)
    #print (edgeList.index(edge) )
    singleLinkEventList[ edgeList.index(event) ].append( i )
    if i%100 == 0:
        print(i)
## singleLinkEvent is a list of lists, which stores every time-stamp an edge had
## an event (has appeared). it corresponds to the edges stored in the edgeList.
#np.random.shuffle(singleLinkEvent)

eventSize = np.zeros(len (singleLinkEventList), dtype = int )

for i in range( len(singleLinkEventList) ):
    eventSize[i] = len(singleLinkEventList[i])

#"""
sortKey = np.argsort(eventSize)
antiSortKey = (np.argsort(sortKey))

singleLinkEventList = list (np.array(singleLinkEventList)[sortKey] )
eventSize = eventSize[sortKey]

#singleLinkEventList = list( np.array(singleLinkEventList)[antiSortKey] )
#eventSize = eventSize[antiSortKey]
#"""

singleLinkEventListCopy = singleLinkEventList.copy()

edgeOccurences = 1
lastJump = 0
summ = 0
for i, singleLinkEvent in enumerate(singleLinkEventList):
    if eventSize[i] != edgeOccurences:
        #print ( eventSize[i] )
        
        edgeOccurences = eventSize[i]
        #print( eventSize[lastJump:i]   )
        sameEventNumEdges = singleLinkEventListCopy[lastJump:i]
        np.random.shuffle( sameEventNumEdges )
        singleLinkEventListCopy[lastJump:i] = sameEventNumEdges 
        #summ += len( eventSize[lastJump:i] )
        lastJump = i
    if i%100 == 0:
        print(i)


singleLinkEventListCopy = list( np.array(singleLinkEventListCopy)[antiSortKey] )
singleLinkEventList = list( np.array(singleLinkEventList)[antiSortKey] )
eventSize = eventSize[antiSortKey]

eventSizeCopy = np.zeros( len(singleLinkEventListCopy), dtype = int )
for i in range( len(singleLinkEventListCopy) ):
    eventSizeCopy[i] = len(singleLinkEventListCopy[i])


for i, eventSeries in enumerate(singleLinkEventListCopy):
    edges [ eventSeries ] = edgeList[ i ] #puts every edge in the new
                                        #timestamps, it has aquired.

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




if (np.sum(eventSizeCopy == eventSize) != len( eventSize )):
    print ( np.sum(eventSizeCopy == eventSize) )
    print(eventSize[(eventSizeCopy == eventSize )== False])
    print(eventSizeCopy[(eventSizeCopy == eventSize )== False])
    print("whaaaat?")
    
for i in range(len(singleLinkEventListCopy)):
    if( len(singleLinkEventListCopy[i]) != len(singleLinkEventList[i]) ):
        print("booo")

