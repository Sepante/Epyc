import importlib as im
import numpy as np
import matplotlib.pyplot as plt
import data_reader as data_1
im.reload(data_1)
#import data_reader as data_2

import time

n = data_1.nrange[data_1.nindex]
ab_cluster_display = True
R_cluster_display = True
a_cluster_display = False

opacity_num = 0.5
binNum = int(n)

hist = np.zeros((data_1.p_size ,binNum), dtype=float)

for qindex in range(data_1.q_size):
    q = data_1.qrange[qindex]
    for pindex in range(data_1.p_size):        
        p = data_1.prange[pindex]
        #print (p,q)
        
        current_data = data_1.data[:, qindex, :]
        #joint_cluster = current_data[joint_condition, 0]
        #joint_cluster = np.sum(current_data[joint_condition, :],1)
        """
        if(R_cluster_display):
            R_cluster = np.sum( data[pindex, qindex, :] ,1)
            hist, bins = np.histogram(R_cluster, bins, range = (0, n))
            widths = np.diff(bins)
            hist = hist / (runNum)
            hist = hist / widths[0]
            plt.bar(bins[:-1], hist, widths,  color = 'r', linewidth=0, alpha = opacity_num)
        """
        
        """ still needs some work (I am not sure what it is)
        if(a_cluster_display):
            single_cluster = current_data[joint_condition, 0] - current_data[joint_condition, 2]
            #single_cluster = current_data[ np.logical_not(joint_conditiosingn) , 0]
            hist, bins = np.histogram(single_cluster, bins, range = (0, n))
            widths = np.diff(bins)
            hist = hist / (runNum)
            hist = hist / widths[0]
            plt.bar(bins[:-1], hist, widths,  color = 'g', linewidth=0, alpha = opacity_num)
        """

        #"""
        if(ab_cluster_display):
            #ab_cluster = current_data[pindex,:,0]
            ab_cluster = np.sum(current_data[pindex],1) #for SIR-SIR
            ab_cluster = current_data[pindex,:,0]+current_data[pindex,:,1] #for SIS-SIR (only considering 
            #                                                               the first two columns from the output)
            #ab_cluster = data_1.data[pindex, qindex, :, 0]
            #ab_cluster = np.sum(data_1.data[pindex, qindex, :, :],1)
            #ab_cluster = np.exp(data_1.data[pindex, qindex, :, 0])
            #print(ab_cluster.max())
            #print(len(ab_cluster))
            
            hist[pindex], bins = np.histogram(ab_cluster, binNum, range = (0, n))
            #plt.bar(bins[:-1], hist[pindex], widths,  color = 'b', linewidth=0, alpha = opacity_num)            
            #print(hist[pindex].sum())
            #print('\n')
        #"""
        """
        name_string = "$normal$, " + dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
        plt.suptitle(name_string)
        plt.xlabel('$mass$')
        plt.ylabel('$P(m)$')

        name_string = name_string.replace('$','')
        plt.ylim([0,0.05])
        plt.xlim([0,n])
        
        plt.savefig(location+name_string+".png")
        
        """
        
    widths = np.diff(bins)
    hist = hist / (data_1.runNum)
    hist = hist / widths[0]
    
    #hist [ hist > 0 ] = 1
    #hist %= 0.06 #for now (be careful)
    #hist = hist**(4)
    #lower_limit = 0.00015
    #lower_limit = 0.1
    #hist[hist < lower_limit] = 1
    upper_limit =0.00001
    hist[hist > upper_limit] = upper_limit
    #hist *=100
    #"""
    im1 = hist.T

    #ax1.imshow(im1, interpolation='none', aspect = 8, cmap=plt.cm.BuPu_r)
    #fig1.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    #cax = plt.axes([0.85, 0.1, 0.075, 0.8])
    #fig1.colorbar(cax=cax)
    #ax1.set_title('5 X 5')
    #"""
    #"""
    plt.subplot(111)
    plt.imshow(im1, interpolation='none', origin = 'lower', aspect = 6/binNum , cmap=plt.cm.Blues)
    #plt.subplot(212)
    #plt.imshow(np.random.random((100, 100)), cmap=plt.cm.BuPu_r)
    

    lam_beta = data_1.prange
    ticks = range(len(lam_beta))
    labels = lam_beta
    
    plt.xticks(ticks, lam_beta, rotation='vertical')
    plt.xlabel('$p$')
    plt.ylabel('$P(ab)$')

    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    cax = plt.axes([0.80, 0.1, 0.035, 0.8])
    plt.colorbar(cax=cax)
    #name_string = "$normal$, " + dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
    #name_string = '$q=p$' + ", $n=$" + str(nrange[nindex]) 
    name_string = '$q=p$' + ", $n=$" + str(128) 
    plt.suptitle(name_string)
    
    name_string = name_string.replace('$','')
    #plt.savefig('/media/sepante/04762A4D762A4032/University/Network Project/Simulation/C++/Temporal SIR/Results/coin-R.png', dpi = 1000) # change the resolution of the saved image
    location = data_1.location
    #plt.savefig(location+" histogram, "+ "ab, " +name_string+".png")
    plt.show()

    
    #"""