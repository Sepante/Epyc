import networkx as nx
from collections import defaultdict
import random
import bisect
import copy

n = 2**10
#n=10
graph = nx.barabasi_albert_graph( n, 5)

nx.write_edgelist(graph,"input_matrix.txt")
print (graph.number_of_edges())
#print (nx.average_degree_connectivity(graph))
#plt.show()
#nx.draw(graph)