import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from data_reader import *


n = nrange[nindex]
#n = 243
norm_data = data / nrange[nindex]
out_break_cond = 0.2 #obtained by the phase plot
opacity_num = 3 / np.sqrt(runNum)
cmap = mpl.cm.rainbow
for qindex in range(q_size):
    q=qrange[qindex]
    outbreak = np.sum(norm_data[:, qindex, :], 2) > 0.01
    outbreak_prob = np.sum(outbreak, 1) / runNum

    plt.plot(prange, outbreak_prob,'-o' , color='black', alpha=1 )
    """
    single_cluster = current_data[ np.logical_not(joint_condition) , 0]
    plt.plot([prange[pindex]], [single_cluster],'o' , color='b', alpha=opacity_num )
    """
    
    #name_string = data_type +"$Phase: $"+" $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[0])
    plt_title = dis_type + ", " + data_type +", $Phase$: $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
    plt.suptitle(plt_title)
    plt.xlabel('$p$')   
    plt.ylabel('$P_{ab}$')
    plt.ylim([0-0.02,1+0.02])
    #plt.xlim([0.01,0.06])
    name_string = plt_title.replace('$','')
    qq = name_string
    location = "results/"
    plt.savefig(location + "p_ab, " + name_string + ".png")
    plt.show()
    #"""
    plt.plot(prange,norm_data[:, qindex, :, 1],'o' , color='black', alpha=opacity_num )
    plt.suptitle(plt_title)
    plt.xlabel('$p$')   
    plt.ylabel('$\\rho_{a}$')
    #plt.xlim([0.03,0.1])
    plt.ylim([0-0.02,1+0.02])
    plt.savefig(location + "rho_a, " + name_string+".png")
    plt.show()
    #"""
    #"""
    plt.plot(prange,norm_data[:, qindex, :, 0],'o' , color='black', alpha=opacity_num )
    plt.suptitle(plt_title)
    plt.xlabel('$p$')   
    plt.ylabel('$\\rho_{ab}$')
    #plt.xlim([0.03,0.1])
    plt.ylim([0-0.02,1+0.02])
    plt.savefig(location + "rho_ab, " + name_string+".png")
    plt.show()
    #"""