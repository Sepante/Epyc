from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


#with open('cdata.txt') as f:
with open('cdata.txt') as f:
    data=[float(i) for i in f]

n_size = int(data.pop(0))
#n = int(data.pop(0))
p_size = int(data.pop(0))
q_size = int(data.pop(0))
#r_size = int(data.pop(0))
runNum = int(data.pop(0))
nrange = [ data.pop(0) for i in range(n_size)]
prange = [ data.pop(0) for i in range(p_size)]
qrange = [ data.pop(0) for i in range(q_size)]
#rrange = [ data.pop(0) for i in range(r_size)]

#data =( np.array(data).reshape(p_size,q_size,runNum) )/n
#n = nrange[0]
data =( np.array(data).reshape(n_size,runNum) )

"""
for i in range(len(qrange)):
    for j in range(runNum):
        plt.plot(prange, data[:,i,j],'-.')
"""
"""
cmap = mpl.cm.rainbow
for nindex in range(n_size):
    n=nrange[nindex]
    for run in range(runNum):
        plt.plot(prange, data[:,qindex,run],'o' , color='b' )
    #plt.suptitle("$2DGrid$ $ q= %.1f$, $N= %d$"%(q,n))
    #plt.suptitle("$Erdos$ $ q= %.1f$, $N= %d$"%(q,n))
    #plt.suptitle("$Phase: $"+" $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[0]))
    plt.suptitle("$Gillespie$ $Erdos$" +"$Phase: $"+" $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[0]))
    plt.xlabel('$p$')
    plt.ylabel('$R$')
    plt.ylim([0-0.02,1+0.02])
    plt.savefig("Phase: "+"n="+str(n)+ ", q=" + str(qrange[qindex]) + ", r=" + str(rrange[0]) + ".png")
    plt.show()
"""
plt.plot(nrange, np.max(data,1),'-o')
name_string = "$Rejection_Based$"+" $Giant Cluster: $"+ ", $p=$" + str(prange[0]) + ", $q=$" + str(qrange[0])
plt.suptitle(name_string)
name_string = name_string.replace('$','')
plt.savefig(name_string+".png")
#plt.plot(nrange, np.max(data,1)/nrange,'-o')