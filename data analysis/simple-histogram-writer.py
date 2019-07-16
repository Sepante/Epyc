import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
#from data_reader import *


nindex = rindex = pindex = qindex = 0
file_dir = "../Results/hist compare/hist-compare-light/"
#file_dir = "../Results/xprotected timed data/primaryschool/"
#file_dir = "../Results/glue_stuff/heteros/"

#file_name = "agg clean sociopattern_conference_contact.txt  non-coop 01e-05 205545703-data.txt"
#file_name = "agg clean sociopattern_conference_contact.txt 1.00e-05 401874239-data.txt"
#file_name = "agg clean sociopattern_conference_contact.txt  non-coop 01e-05 205545703-data.txt"
#file_name = "Erdos 1.25e-05 413026351-data.txt"
#file_name = "hospital/D-sh clean sociopattern_hospital 0.0100.txt"
#file_names = ["hospital/clean sociopattern_hospital 0.0100.txt",
        #"hospital/D-sh clean sociopattern_hospital 0.0100.txt",
              #"hospital/DCB-sh clean sociopattern_hospital 0.0100.txt",
              #"hospital/DCW-sh clean sociopattern_hospital 0.0100.txt",
              #"hospital/DCWB-sh clean sociopattern_hospital 0.0100.txt",
              #]
file_names = ["clean sociopattern_hospital.txt q=1.txt",
              "SO-sh clean sociopattern_hospital.txt 0.01 1556295241-data.txt",
              "DCW-sh clean sociopattern_hospital.txt q=1-data.txt",
              "DCWB-sh clean sociopattern_hospital.txt q=1-data.txt",
              "D-sh clean sociopattern_hospital.txt 0.01-data.txt",
              "DCB-sh clean sociopattern_hospital.txt q=1-data.txt",
              ]              
              
pd_hists = pd.DataFrame()
#file_name = "SO-sh clean sociopattern_hospital.txt 0.06 2010498520-data.txt"

for file_name in file_names:    
    with open(file_dir + file_name, 'r') as f:
    
    #with open('../Results/bursty grid 0.15.txt 1380287758-data.txt') as f:
    
        dis_type=(f.readline())
        data_type=(f.readline())
        dis_type = dis_type.replace('\n','')
        data_type = data_type.replace('\n','')
        
        n_size = int(f.readline())
        p_size = int(f.readline())
        q_size = int(f.readline())
        r_size = int(f.readline())
        
            
        runNum = int(f.readline())
        nrange = [ int(f.readline()) for i in range(n_size)]
        prange = [ float(f.readline()) for i in range(p_size)]
        qrange = [ float(f.readline()) for i in range(q_size) ]
        rrange = [ float(f.readline()) for i in range(r_size) ]
        
        
        pd_data = pd.read_csv(f)
    if ( 'non-coop' in str(f) ):
        qrange = prange
    data = np.array(pd_data)
    data = np.array(data).reshape(p_size, q_size, runNum,3)
    
    location = "../Results/"
    
    n = nrange[nindex]
    
    #name_string = dis_type + ", " + data_type + ", $n=$" + str(nrange[-1]) + ", $p=$" + str(prange[-1]) + ", $q=$" + str(qrange[-1]) + ", $r=$" + str(rrange[-1])
    name_string = dis_type + ", " + data_type + ", $n=$" + str(nrange[-1]) + ", $p=$" + str(prange[-1]) + ", $q=$" + str(qrange[-1]) + ", $r=$" + str(rrange[-1])
            
    joint_cluster = data[-1, -1, :, 0] #only consider last p, q values.
                                        #only consider last p, q values.
                                        #only consider last p, q values.
                                        #only consider last p, q values.
    
    hist, bins = np.histogram(joint_cluster, int(n/1), range = (0, n))
    widths = np.diff(bins)
    hist = hist / (runNum)
    hist = hist / widths[0]
    #plt.bar(bins[:-1], hist, widths,  color = 'g', alpha = 1, ec='black')
            
            
    
    #plt.suptitle(name_string)
    #plt.xlabel('$mass$')
    #plt.ylabel('$P(m)$')
    
    name_string = name_string.replace('$','')
    data_type = data_type.replace('$', '')
    data_type = data_type.replace('.txt', '')
    #plt.ylim([0,0.06])
    #plt.xlim([0,n])
    
    #plt.savefig(location+name_string+".png" , bbox_inches='tight')
    #plt.show()
    

    pd_hists[data_type] = hist

    print(data_type)

pd_hists.to_csv( location + "hist compare/" + name_string+".hist", header = True , index = None , sep = ',' )    
    #with open(location + name_string+".hist", 'w') as f:
         
        #f.write("vertices:\t" + str(vertices_num) + '\n')
        #f.write("edge average:\t" + str(edge_average))
#histMin = np.min(pd_hists)
histMin = np.sort(list(set(np.min(pd_hists,1))))[1] #crazy temporary way to find
                                                    #the lowest non-zero value.
crossEntropy = []
    
for dataType in pd_hists.columns[1:]:
    crossEnt = stats.entropy(pd_hists [pd_hists.columns[0]]+histMin, pd_hists[dataType]+histMin)
    crossEntropy.append(crossEnt)

x = range( len(file_names) - 1 )
plt.bar( x, crossEntropy)
graphType = "$hospital$" #temporary
plt.title(graphType +" cross entropy distance from original data")
plt.xticks(x, ["SO", "DCW", "DCWB", "D", "DCB"])
#plt.savefig("cross-entropy.png")