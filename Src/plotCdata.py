from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


with open('cdata.txt') as f:
    #for i in range(1):
    dis_type=(f.readline())
    data_type=(f.readline())
    
    data=[float(i) for i in f]

n_size = int(data.pop(0))
#n = int(data.pop(0))
p_size = int(data.pop(0))
q_size = int(data.pop(0))
r_size = int(data.pop(0))
runNum = int(data.pop(0))
nrange = [ data.pop(0) for i in range(n_size)]
prange = [ data.pop(0) for i in range(p_size)]
qrange = [ data.pop(0) for i in range(q_size)]
rrange = [ data.pop(0) for i in range(r_size)]

#data =( np.array(data).reshape(p_size,q_size,runNum) )/n
n = nrange[0]
#n = 243
data =( np.array(data).reshape(p_size, q_size, runNum) )/n

"""
for i in range(len(qrange)):
    for j in range(runNum):
        plt.plot(prange, data[:,i,j],'-.')
"""
opacity_num = 200 * 1/runNum
cmap = mpl.cm.rainbow
for qindex in range(q_size):
    q=qrange[qindex]
    #for run in range(runNum):
        #plt.plot(prange, data[:,qindex,run],'o' , color='g', alpha=opacity_num )
    plt.plot(prange, data[:,qindex,:],'o' , color='g', alpha=opacity_num )

    #data_type = " $Primary$ $School: $"
    dis_type = dis_type.replace('\n','')
    data_type = data_type.replace('\n','')
    #name_string = data_type +"$Phase: $"+" $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[0])
    name_string = dis_type + ", " + data_type +", $Phase$: $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[0])
    plt.suptitle(name_string)
    plt.xlabel('$p$')   
    plt.ylabel('$R$')
    plt.ylim([0-0.02,1+0.02])
    #plt.ylim([0.8,1+0.02])*=
    name_string = name_string.replace('$','')
    
    
    location = "results/"
    #plt.savefig(location+name_string+".png")
    plt.show()