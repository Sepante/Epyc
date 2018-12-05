import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.stats import expon
import scipy.stats as st
import pandas as pd
from collections import Counter


#input_file_address = "network data/original/"
output_file_address = "../network data/bursty grid/"


N = 20000
vertices_num = 100
#N = 1000
ld = 0.2
#cnct = expon.rvs(size=N, loc = 0.1, scale = 0.9)
#cnct = expon.rvs(size=N, loc = 1, scale = 0)
#cnct = np.random.poisson(ld, N)/ld
#cnct = (np.random.binomial(n, p, N)/(n*p))

#cnct = np.random.lognormal( np.log(np.e), 0.78, N)
cnct = np.random.lognormal( np.log(np.e), 2, N)
#cnct = np.random.lognormal( np.log(np.e),3, N)

#cnct = st.lognorm.rvs( 1, 1 , size=N )
#cnct = st.powerlaw.rvs( 100000, -1, size=N )
#cnct = np.random.lognormal(np.log10(10000),2,N)
cnct = np.round(cnct,0)
cnct /= cnct.mean()


graph = np.zeros((N, 3), int)

#graph[:, 0] = np.cumsum(cnct)*(10)
graph[:, 0] = np.cumsum(cnct)
graph[:, 0] -= graph[0, 0]

"""
plt.plot(graph[:, 0], np.ones(N),'o',alpha = 20/N)
#plt.plot(cnct,'o')
#plt.xlim([0,N])
#plt.show()

print (cnct.min())
print (np.mean(cnct))
print (np.std(cnct))
#print('\n')

print("burst = ",burst)
"""
L = np.sqrt(vertices_num) #length of grid side
cnct = np.diff(graph[:,0])
burst = ( np.std(cnct) - np.mean(cnct) ) / (np.std(cnct) + np.mean(cnct) )
graph[:, 1] = np.random.randint(0,vertices_num,N) #first node
graph[:, 2] = ( graph[:, 1] + np.random.choice([1,L], N) ) % vertices_num #second node has to be one to the right or one, bellow the first node.
#"""
#output = open('burst_graph.txt', 'w')

t_respect_graph = pd.DataFrame(graph)
burst_str = '{0:04.2f}'.format( burst.round(2) )
output_file_name = "bursty grid " + burst_str + ".txt"
output_file_info = output_file_address + "info " + output_file_name
#t_respect_graph.to_csv('burst_graph.txt',index = False, header = False, sep = '\t')

content = t_respect_graph.to_csv( output_file_address + output_file_name, header = None , index = None , sep = '\t' )

edge_average = len(graph) / (graph[-1, 0] - graph[0, 0])

with open(output_file_info, 'w') as f:
    f.write("vertices:\t" + str(vertices_num) + '\n')
    f.write("edge average:\t" + str(edge_average))

print("burst = ",burst)
#"""