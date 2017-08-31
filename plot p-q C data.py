from __future__ import division
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import copy as cp

def binned( data, xmin, xmax, binNum, log = False):
    if(log):
        print log
        data = np.log10(data)
        xmax = np.log10(xmax)
        xmin = np.log10(xmin)
    bin_array = np.zeros(binNum)
    binLen = (xmax-xmin)/binNum
    #print xmax
    #print xmin
#    print ("binLen=",binLen)
    for x in data:
        xbin=int((x-xmin)/binLen)
        #print xbin
        if x==xmax:
            xbin-=1
        bin_array[xbin]+=1
        
    return np.array([np.arange(xmin, xmax, binLen) ,bin_array])


#"""
with open('cdata.txt') as f:
    data=[float(i) for i in f]


n = int(data.pop(0))
p_size = int(data.pop(0))
q_size = int(data.pop(0))
runNum = int(data.pop(0))
prange = [ data.pop(0) for i in range(p_size)]
qrange = [ data.pop(0) for i in range(q_size)]


#"""
data =( np.array(data) )


#plt.hist(data, bins=np.logspace(0, np.log10(n),10 )  )
#"""
plt.hist(data, bins=np.logspace(0, np.log10(np.max(data)),100 ) )
plt.gca().set_xscale("log")
#plt.ylim([1,100000])
plt.gca().set_yscale("log")
plt.suptitle("$Erdos$, $p= %.2f$, $q= %.1f$, $N= %d$"%(prange[0],qrange[0],n))
plt.xlabel('$mass$')
plt.ylabel('$P(m)$')
plt.show()
#"""
#data = np.array([1,2,3,4])
#Q =( binned(data,np.min(data),np.max(data), 10, True) )
#plt.gca().set_xscale("log")
#plt.gca().set_yscale("log")
#plt.ylim([0,10])
#plt.plot(Q[0],Q[1])