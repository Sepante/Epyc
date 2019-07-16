import numpy as np
import matplotlib.pyplot as plt
from data_reader import *

#from data_reader import datareader
#import data_reader
n = nrange[nindex]

name_string = "$normal$, " + dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
#n=243
opacity_num = 0.5

#for pindex in range(p_size):
    #for qindex in range(q_size):
for pindex in [-1]:
    for qindex in [-1]:
        
        current_data = data[pindex, qindex, :]
        
        #high_a = current_data[:, 1] > -1
        #high_b = current_data[:, 2] > -1
        #joint_condition = np.logical_and(high_a, high_b)
        #joint_cluster = current_data[joint_condition, 0]
        #joint_cluster = np.sum(current_data[joint_condition, :],1)
        #joint_cluster = np.sum( data[pindex, qindex, :] , 1)
        joint_cluster = data[pindex, qindex, :, 0]

        #joint_cluster = joint_cluster[::2]
        #joint_cluster = joint_cluster[y_pred == 0]


        hist, bins = np.histogram(joint_cluster, int(n/1), range = (0, n))
        widths = np.diff(bins)
        hist = hist / (runNum)
        hist = hist / widths[0]
        plt.bar(bins[:-1], hist, widths,  color = 'g', alpha = 1, ec='black')
        plt.show()
        
        
        
        
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

        
        plt.suptitle(name_string)
        plt.xlabel('$mass$')
        plt.ylabel('$P(m)$')

        name_string = name_string.replace('$','')
        plt.ylim([0,0.06])
        plt.xlim([0,n])
        
        #plt.savefig(location+name_string+".png" , bbox_inches='tight')
        #plt.show()

pd_data = pd.DataFrame()
pd_data[data_type] = hist
pd_data.to_csv( location + "hist compare/" + name_string+".hist", header = True , index = None , sep = ',' )
print(data_type)

#with open(location + name_string+".hist", 'w') as f:
     
    #f.write("vertices:\t" + str(vertices_num) + '\n')
    #f.write("edge average:\t" + str(edge_average))
