import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

with open('cdata.txt') as f:
    #for i in range(1):
    dis_type=(f.readline())
    data_type=(f.readline())
    
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

data = np.array(pd_data)
data = np.array(data).reshape(p_size, q_size, runNum,3)
nindex = rindex = pindex = 0
    #print(f)
"""
opacity_num =  500/runNum
opacity_num =  1
#cmap = mpl.cm.rainbow
for qindex in range(q_size):
    q=qrange[qindex]
    n = nrange[0]
    #for run in range(runNum):
        #plt.plot(prange, data[:,qindex,run],'o' , color='g', alpha=opacity_num )
    plt.plot(prange, [data],'o' , color='g', alpha=opacity_num )

    #data_type = " $Primary$ $School: $"
    dis_type = dis_type.replace('\n','')
    data_type = data_type.replace('\n','')
    #name_string = data_type +"$Phase: $"+" $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[0])
    name_string = dis_type + ", " + data_type +", $Phase$: $n=$"+str(n)+ ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[0])
    plt.suptitle(name_string)
    plt.xlabel('$p$')   
    plt.ylabel('$R$')
    #plt.xlim([0.03,0.1])
    #plt.ylim([0-0.02,1+0.02])
    #plt.ylim([0.2, 1])
    #plt.ylim([0.8,1+0.02])*=
    name_string = name_string.replace('$','')
    
    
    location = "results/"
    #plt.savefig(location+name_string+".png")
    plt.show()
"""