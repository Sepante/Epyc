import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

file_dir = "../Results/xprotected seed data/primaryschool/"
file_name = "giant clean primaryschool.txt 0.145 603472209-data.txt"
with open( file_dir + file_name  ) as f:
#with open( '../Results/xprotected seed data/DCWB-sh giant clean primaryschool.txt 0.145 223390942-data.txt' ) as f:



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

nindex = pindex = qindex = rindex = 0


if ( 'non-coop' in file_name ):
    qrange = prange

#plt.yscale('log')
#plt.plot(pd_data['t'], pd_data['B'] )
#plt.plot(pd_data['t'], pd_data['AB'] )
#pd_data['Aave']
#plt.plot(pd_data['t'], pd_data['ab'] )
#data = np.array(data).reshape(p_size, q_size, runNum,3)
#plt.xlim([300,500])
#nindex = rindex = pindex = qindex = 0
#location = "../Results/"
#plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
#plt.plot(pd_data[[' b_cluster','seed']].groupby('seed').mean() , label='AB(t)', markeredgewidth=0 )
plt.hist(np.array(pd_data[[' ab_cluster','seed']].groupby('seed').mean())[:,0], 50, density  = True,  ec='black')
name_string = name_string = "$normal$, " + dis_type + ", " + data_type +  "\n$n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])

plt.suptitle(name_string, fontsize = 10)
#plt.savefig(name_string + "mean hist.png" , bbox_inches='tight')