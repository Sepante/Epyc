import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix

time_file_name = file_name.split(' ')[-1]
time_file_name = time_file_name.replace('-data', ' timed-data')

pd_data = pd.read_csv(file_dir + time_file_name)
if ( 'non-coop' in file_name ):
    qrange = prange

plot = True

#pd_data_DCWB = pd.read_csv("../Results/1851548799 timed-data.txt")        
#pd_data_DCWB_non = pd.read_csv("../Results/2101799709 timed-data.txt")
#pd_data_non = pd.read_csv("../Results/891059992 timed-data.txt")

#data = np.array(pd_data)
#plt.plot(pd_data['t'], pd_data['a'], 'o', alpha = 0.005)
#"""
if plot:
    plt.plot(pd_data['t'], pd_data['A'], alpha = 0.5, linewidth = 0.3)
    plt.plot(pd_data['t'], pd_data['AB'], alpha = 0.5, linewidth = 0.3)
#""" 
#plt.plot(pd_data['t'], pd_data['A'])
#plt.plot(pd_data['t'], pd_data['B'])


#plt.xlim([0,40000])
#plt.ylim([1,2000])

#plt.plot(pd_data_DCWB['t'], pd_data_DCWB['AB'], alpha = 1)
#plt.yscale('log')
#plt.show()
#plt.plot(pd_data[['A','t']].groupby('t').mean() , label='A(t)', markeredgewidth=0 )

#plt.plot(pd_data_DCWB[['AB','t']].groupby('t').mean() , label='DCWB AB(t)', markeredgewidth=0 )
"""
if plot:
    #plt.plot(pd_data[['A','t']].groupby('t').mean(), 'b' , label='average A(t)', markeredgewidth=0, linewidth = 3 )
    plt.plot(pd_data[['AB','t']].groupby('t').mean(), 'orange' , label='average AB(t)', markeredgewidth=0, linewidth = 3 )
"""
#plt.plot(pd_data[['B','t']].groupby('t').mean() , label='B(t)', markeredgewidth=0 )
#plt.xlim([0, 100000])
#plt.plot(pd_data[['a','t']].groupby('t').mean() , label='a(t)', markeredgewidth=0 )
#plt.plot(pd_data[['ab','t']].groupby('t').mean() , label='ab(t)', markeredgewidth=0 )

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
if plot:
    plt.legend()
    name_string = name_string = "$normal$, " + dis_type + ", " + data_type +  "\n$n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
    plt.title(name_string, fontsize = 10)
    #plt.text(0,5,0.5,"hey")
    
    
    plt.savefig(name_string+"timed.png" , bbox_inches='tight')