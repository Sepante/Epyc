import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
#from data_reader import *

binSize = 6

nindex = rindex = pindex = qindex = 0
#file_dir = "../Results/hist compare/hist-compare-light/"
#file_dir = "../Results/xprotected timed data/primaryschool/"
file_dir = "../Results/glue_stuff/heteros/conference/coop/"
file_dir = "../Results/glue_stuff/heteros/primaryschool-adjusted/coop/"

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
for root, dirs, file_names in os.walk(file_dir, topdown=False):
    #print(files)
    True
#print(files)
#"""

labels = []
original_ind = 0
for i, file in enumerate( file_names ):
    label = file.split(' ')[0]
    labels.append( label )
    if (label == 'clean' or label == 'giant'):
        original_ind = i

labels[0], labels[original_ind] = labels[original_ind], labels[0]
file_names[0], file_names[original_ind] = file_names[original_ind], file_names[0]

graphType = file.split('.txt')[0]
graphType = graphType.split('clean ')[-1]
graphType = graphType.split(' ')[0]

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
    
    hist, bins = np.histogram(joint_cluster, int(n/binSize), range = (0, n))
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

    #print(data_type)

pd_hists.to_csv( location + "hist compare/" + name_string+".hist", header = True , index = None , sep = ',' )    
    #with open(location + name_string+".hist", 'w') as f:
         
        #f.write("vertices:\t" + str(vertices_num) + '\n')
        #f.write("edge average:\t" + str(edge_average))
#histMin = np.min(pd_hists)

histMin = np.sort(list(set(np.min(pd_hists,1))))[1] #crazy temporary way to find
                                                    #the lowest non-zero value.
crossEntropy = []
    
for dataType in pd_hists.columns[1:]:
    print(dataType)
    crossEnt = stats.entropy( (pd_hists [pd_hists.columns[0]]+histMin) / (1 + histMin), (pd_hists[dataType]+histMin) / (1 + histMin) )
    crossEntropy.append(crossEnt)

x = range( len(file_names) - 1 )

crossEntropy = np.array(crossEntropy)


qtext = str(qrange[-1])
if ( 'non-coop' in str(f) ):
    qtext = 'p'


name_string = graphType + " cross entropy distance from original data"\
+ ", " + "\n" +\
", $n=$" + str(nrange[-1]) + ", $p=$" + str( prange[-1] )\
+ ", $q=$" + qtext + ", $r=$" + str(rrange[-1])


plt.title( name_string )

shuffle_labels = np.array( labels[1:] )
sort_ind = np.argsort( shuffle_labels )
shuffle_labels = shuffle_labels[sort_ind]
crossEntropy = crossEntropy[sort_ind]
"""
sort_ind = np.argsort( crossEntropy )
crossEntropy = crossEntropy[sort_ind]
shuffle_labels = shuffle_labels[sort_ind]
"""

plt.bar( x, crossEntropy)
plt.xticks(x, shuffle_labels)
location = "../Results/crossEntropy/"
plt.savefig( location + graphType + " q=" + qtext + " cross-entropy.png")
#"""
file_name =  location + "totalCrossEntropy.csv"
with open(file_name, "a") as f:
    DF = pd.DataFrame([crossEntropy] , index = [graphType], columns = shuffle_labels)
    file_empty = (os.stat(file_name).st_size == 0)
    if file_empty:
        DF.to_csv(f)
    else:
        DF.to_csv(f, header = False)
#"""