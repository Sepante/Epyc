import networkx as nx
import numpy as np

n = 2**8
#n=10
cnct_prob = 4/n
G = nx.erdos_renyi_graph( n, cnct_prob)
edge_list=[]
for line in nx.generate_edgelist(G, data=False):
    edge_list.append(line)
#nx.write_edgelist(graph,"input_matrix.txt")
    
f = open('input_matrix.txt', 'w')
time = 0
times = []
for i in range(100000):
    #print (i)
    time += np.random.exponential(1)
    times.append(time)
    edge = np.random.choice(edge_list)
    string = str(int(time)) + ' ' + edge  + '\n'
    #string = str(int(i/2)) + ' ' + edge  + '\n'
    print (string)
    f.write(string)

times = np.array(times)
#diffs = np.diff(times)
m = np.mean(times)
s = np.std(times)
b = (s-m)/(s+m)
print (b)
#print (graph.number_of_edges())
#print (nx.average_degree_connectivity(graph))
#plt.show()
#nx.draw(graph)