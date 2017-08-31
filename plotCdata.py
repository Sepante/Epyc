from __future__ import division
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import copy as cp


with open('cdata.txt') as f:
    data=[float(i) for i in f]


n = int(data.pop(0))
p_size = int(data.pop(0))
q_size = int(data.pop(0))
runNum = int(data.pop(0))
prange = [ data.pop(0) for i in range(p_size)]
qrange = [ data.pop(0) for i in range(q_size)]


#data =( np.array(data).reshape(p_size,q_size,runNum) )/n
data =( np.array(data).reshape(p_size, q_size, runNum) )/n

"""
for i in range(len(qrange)):
    for j in range(runNum):
        plt.plot(prange, data[:,i,j],'-.')
"""
cmap = mpl.cm.rainbow
for i in range(q_size):
    for j in range(runNum):
        plt.plot(prange, data[:,i,j],'o' , color=cmap(1/(i+1)) )
        plt.show()
        #plt.plot(prange, data[:,0,j], color=cmap(0.24) )