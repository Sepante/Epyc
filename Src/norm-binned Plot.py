import numpy as np
import matplotlib.pyplot as plt
#from data_reader import datareader
#import data_reader

"""
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
n = nrange[nindex]
#n = 100
"""
n=243
opacity_num = 0.5
for pindex in range(p_size):
    for qindex in range(q_size):
        #n = nrange[nindex]

        current_data = data[pindex, qindex, :]
        
        high_a = current_data[:, 1] > 30
        high_b = current_data[:, 2] > 30
        joint_condition = np.logical_and(high_a, high_b)
        joint_cluster = current_data[joint_condition,0]


        hist, bins = np.histogram(joint_cluster, n, range = (0, n))
        widths = np.diff(bins)
        hist = hist / (runNum)
        hist = hist / widths[0]
        #print(hist)
        plt.bar(bins[:-1], hist, widths,  color = 'r', linewidth=0, alpha = opacity_num)


        #plt.ylim([0, 10])
        #"""
        single_cluster = current_data[ np.logical_not(joint_condition) , 0]
        hist, bins = np.histogram(single_cluster, n, range = (0, n))
        widths = np.diff(bins)
        hist = hist / (runNum)
        hist = hist / widths[0]
        plt.bar(bins[:-1], hist, widths,  color = 'b', linewidth=0, alpha = opacity_num)
        #"""

        #plt.xlim([400,512])
        """nice one!"""
        
        
        #q=plt.hist( current_data, 300, normed=True, color = 'b', edgecolor='b', alpha = opacity_num)
        #q=plt.hist( current_data, n, normed=True, color = 'b' )
        
        dis_type = dis_type.replace('\n','')
        data_type = data_type.replace('\n','')
        name_string = "$normal$, " + dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
        plt.suptitle(name_string)
        plt.xlabel('$mass$')
        plt.ylabel('$P(m)$')

        location = "results/"
        name_string = name_string.replace('$','')
        plt.ylim([0,0.01])
        plt.xlim([0,n])
        
        plt.savefig(location+name_string+".png")
        plt.show()
        

#plt.show()
#data = np.array(data)
#high_clust = data > 300
#xdata = data[high_clust]
#print(np.mean(data))
