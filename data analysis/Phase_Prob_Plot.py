import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import importlib as im
import data_reader
im.reload(data_reader)
from data_reader import *



n = nrange[nindex]
#n = 243
norm_data = data / n

outbreak_prob = np.zeros(p_size)

outbreak_cond = 0.6 #obtained by the phase plot
opacity_num = 3 / np.sqrt(runNum)
cmap = mpl.cm.rainbow
for qindex in range(q_size):
    q=qrange[qindex]
    for pindex in range(p_size):

        #outbreak = np.sum(norm_data[:, qindex, :], 2) > outbreak_cond
        #outbreak_prob = np.sum(outbreak, 1) / runNum
        current_data = norm_data[pindex, qindex, :]
        # for investigating SIS nodes, because there are many cases which the disease dies out
        #, have a disproportional effect on the ensemble and have to be carved out.
        #current_data = current_data [current_data[ :, 2 ] < 0.1]
        current_data = current_data [current_data[ :, 2 ] != 0]
        
        #joint_cluster = current_data[:, 0] + current_data[:, 1] +current_data[:, 2]
        joint_cluster = current_data[:, 0] + current_data[:, 1] 
        outbreak_prob[pindex] = np.sum(joint_cluster > outbreak_cond) / len(joint_cluster)

    plt.plot(prange, outbreak_prob,'-o' , color='black', alpha=1 )
    """
    single_cluster = current_data[ np.logical_not(joint_condition) , 0]
    plt.plot([prange[pindex]], [single_cluster],'o' , color='b', alpha=opacity_num )
    """
    
    plt_title = dis_type + ", " + data_type +", $Phase$: $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
    plt.suptitle(plt_title)
    plt.xlabel('$p$')   
    plt.ylabel('$P_{outbreak}$')
    plt.ylim([0-0.00,0.170])
    #plt.xlim([0.01,0.06])
    name_string = plt_title.replace('$','')
    #qq = name_string
    plt.grid()
    plt.savefig(location + "p_ab, " + name_string + ".png")
    plt.show()
    """

    plt.plot(prange,norm_data[:, qindex, :, 1],'o' , color='black', alpha=opacity_num )
    plt.suptitle(plt_title)
    plt.xlabel('$p$')   
    plt.ylabel('$\\rho_{a}$')
    #plt.xlim([0.03,0.1])
    plt.ylim([0-0.02,1+0.02])
    plt.savefig(location + "rho_a, " + name_string+".png")
    plt.show()
    #"""
    """
    plt.plot(prange,norm_data[:, qindex, :, 0],'o' , color='black', alpha=opacity_num )
    plt.suptitle(plt_title)
    plt.xlabel('$p$')   
    plt.ylabel('$\\rho_{ab}$')
    #plt.xlim([0.03,0.1])
    plt.ylim([0-0.02,1+0.02])
    plt.savefig(location + "rho_ab, " + name_string+".png")
    plt.show()
    #"""