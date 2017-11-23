import numpy as np
import matplotlib.pyplot as plt
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
nrange = [ int(data.pop(0)) for i in range(n_size)]
prange = [ data.pop(0) for i in range(p_size)]
qrange = [ data.pop(0) for i in range(q_size)]
rrange = [ data.pop(0) for i in range(r_size)]

#print (data.count(50))
data =( np.array(data).reshape(p_size, q_size, runNum) )
nindex = 0
rindex = 0
"""this has to get checked"""
n = 243
for pindex in range(p_size):
    for qindex in range(q_size):
        #n = nrange[nindex]
        current_data = data[pindex, qindex, :]
        #q=plt.hist( current_data, n, normed=True )
        q=plt.hist( current_data, 1000, normed=True )
        dis_type = dis_type.replace('\n','')
        data_type = data_type.replace('\n','')
        name_string = "$normal$, " + dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
        plt.suptitle(name_string)
        plt.xlabel('$mass$')
        plt.ylabel('$P(m)$')
        
        location = "results/"
        name_string = name_string.replace('$','')
        plt.ylim([0,0.05])
        #plt.xlim([50,250])
        plt.savefig(location+name_string+".png")
        plt.show()

#plt.show()
data = np.array(data)
high_clust = data > 300
xdata = data[high_clust]
#print(np.mean(data))
