import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from data_reader import *

matplotlib.rcParams.update({'font.size': 15})


#from data_reader import datareader
#import data_reader
n = nrange[nindex]
node_number_normalized = True

name_string = "$normal$, " + dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
#n=243
opacity_num = 0.5

fig = plt.figure()
#ax = fig.add_subplot(1,1,1)

#for pindex in range(p_size):
for pindex in [-1]:
    p = prange[pindex]
    #for qindex in range(q_size):
#for pindex in [0, 10, 20, 30, 40, 50, 59]:
    for qindex in [-1]:
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        
        
        #current_data = data[pindex, qindex, :]
        
        #high_a = current_data[:, 1] > -1
        #high_b = current_data[:, 2] > -1
        #joint_condition = np.logical_and(high_a, high_b)
        #joint_cluster = current_data[joint_condition, 0]
        #joint_cluster = np.sum(current_data[joint_condition, :],1)
        #joint_cluster = np.sum( data[pindex, qindex, :] , 1)
        joint_cluster = data[pindex, qindex, :, 0]
        #joint_cluster = data[pindex, qindex, :, 1]

        #joint_cluster = joint_cluster[::2]
        #joint_cluster = joint_cluster[y_pred == 0]

            #cs = ax.imshow(im1, interpolation='none', origin = 'lower', aspect = aspect , cmap=plt.cm.gnuplot , extent =[prange[0],prange[-1],  1 + omitted_bins * binLen ,  n ] )

        hist, bins = np.histogram(joint_cluster, int(n), range = (0, n))
        
        widths = np.diff(bins)
        hist = hist / (runNum)
        hist = hist / widths[0]

        if node_number_normalized:
            bins /= n

        #ax.bar(bins[:-1], hist, widths,  color = 'orange', alpha = 1, ec='black')
        ax.fill(hist, bins[:-1], color = 'orange')
        #plt.xlim([20/n,500/n])
        #plt.ylim([0, 2])
        #plt.show()
        
        
        
        
        """
        single_cluster = current_data[joint_condition, 0] - current_data[joint_condition, 2]
        #single_cluster = current_data[ np.logical_not(joint_conditiosingn) , 0]
        hist, bins = np.histogram(single_cluster, n, range = (0, n))
        widths = np.diff(bins)
        hist = hist / (runNum)
        hist = hist / widths[0]
        plt.bar(bins[:-1], hist, widths,  color = 'b', linewidth=0, alpha = opacity_num)
        """

        """
        all_cluster = current_data[ : , 0]
        hist, bins = np.histogram(all_cluster, n, range = (0, n))
        widths = np.diff(bins)
        hist = hist / (runNum)
        hist = hist / widths[0]
        plt.bar(bins[:-1], hist, widths,  color = 'b', linewidth=0, alpha = opacity_num)
        """

        
        #ax.set_title(name_string)
        ax.set_ylabel('$ \\rho_{ab} $')
        ax.set_xlabel('$\Pi( \\rho_{ab} )$')
        name_string = name_string.replace('$','')
        
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        ax.yaxis.major.formatter._useMathText = True

        ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
        ax.xaxis.major.formatter._useMathText = True

        #ax.set_aspect('equal')9
        #plt.ylim([0,0.06])
        #plt.xlim([0, 0.01])


        ax.set_ylim([0.2133*1, 1])
        ax.set_xlim([0, 0.015])
        ax.set_aspect(1/ax.get_data_ratio())
        
        fig.savefig('hist-'+str(prange[pindex]).replace('.','')+'.png', dpi = 300, bbox_inches='tight')
        #plt.savefig(location+name_string+".png" , bbox_inches='tight')
        plt.show()

#pd_data = pd.DataFrame()
#pd_data[data_type] = hist
#pd_data.to_csv( location + "hist compare/" + name_string+".hist", header = True , index = None , sep = ',' )
#print(data_type)

#with open(location + name_string+".hist", 'w') as f:
     
    #f.write("vertices:\t" + str(vertices_num) + '\n')
    #f.write("edge average:\t" + str(edge_average))
