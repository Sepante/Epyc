import importlib as im
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


import data_reader
im.reload(data_reader)
from data_reader import *

import time
from sklearn.cluster import MeanShift, estimate_bandwidth
#"""

#n = 243
n = nrange[nindex]
norm_data = data / n

#opacity_num =  200/runNum
opacity_num = 0.01
cmap = mpl.cm.rainbow
for qindex in range(q_size):
    q=qrange[qindex]
    for pindex in range(p_size):
        current_data = norm_data[pindex, qindex, :]
            
        #high_a = current_data[:, 1] > 0.02
        #high_b = current_data[:, 2] > 0.02
        #joint_condition = np.logical_and(high_a, high_b)
        #joint_cluster = current_data[joint_condition,0]
        #joint_cluster = np.sum(current_data[:,:],1)
        #joint_cluster = current_data[:, 1]
        
        joint_cluster = current_data[:, 0] + current_data[:, 1]
        #joint_cluster = joint_cluster [::5]
        joint_cluster.sort()
        plt.plot([prange[pindex]], [joint_cluster],'o' , color='purple', alpha=opacity_num )
        """
        single_cluster = current_data[ np.logical_not(joint_condition) , 0]
        plt.plot([prange[pindex]], [single_cluster],'o' , color='b', alpha=opacity_num )
        """

        #name_string = data_type +"$Phase: $"+" $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[0])
        name_string = dis_type + ", " + data_type +", $Phase$: $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
        """plt.suptitle(name_string)
        plt.xlabel('$p$')   
        plt.ylabel('$R$')
        #plt.xlim([0.03,0.1])
        plt.ylim([0-0.02,1+0.02])
        #plt.xlim([0.01,0.06])
        #plt.ylim([0.2, 1])
        """
        name_string = name_string.replace('$','')
        """
        X = np.zeros((len( joint_cluster ),2), dtype = np.float)
        X[:,0] = joint_cluster
        #X = np.array(zip(x,np.zeros(len(x))), dtype=np.int)
        
        
        #X = list(zip(x,np.zeros(len(x))))
        
        bandwidth = estimate_bandwidth(X, quantile=0.3)
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(X)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_
        
        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)
        n_clusters_ = 2
        aves = np.zeros(n_clusters_)
        for k in range(n_clusters_):
            my_members = labels == k
            #print ( "cluster {0}: {1}".format(k, X[my_members, 0]) )
            #print (X[k].mean())
            aves[k] = X[my_members].mean()
        #plt.plot( aves, 'o' )
        """
        aves = np.zeros(2)
        split_indice = np.diff(np.sort(joint_cluster)).argmax()
        aves [0] = joint_cluster[:split_indice].mean()
        aves [1] = joint_cluster[split_indice:].mean()
        print(split_indice)
        print(aves)
        plt.plot([prange[pindex]], [aves],'bo', alpha=1 )
        plt.plot([prange[pindex]], [[joint_cluster[split_indice]]],'ro', alpha=1 )
        

    #plt.savefig(location + name_string+".png")
    plt.show()#"""
#ab_cluster = [1,1,5,6,1,5,10,22,23,23,50,51,51,52,100,112,130,500,512,600,12000,12230]

