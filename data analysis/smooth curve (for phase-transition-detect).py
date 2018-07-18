import importlib as im
import data_reader
im.reload(data_reader)
from data_reader import *

from sklearn.grid_search import GridSearchCV


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.neighbors import KernelDensity
from sklearn.cluster import estimate_bandwidth

n = nrange[nindex]
norm_data = data / n
opacity_num = 0.5

for pindex in range(p_size):
#for pindex in range(1):

    current_data = norm_data[pindex, qindex, :]
    
    # for investigating SIS nodes, because there are many cases which the disease dies out
    #, have a disproportional effect on the ensemble and have to be carved out.
    #current_data = current_data [current_data[ :, 2 ] < 0.1]
    current_data = current_data [current_data[ :, 2 ] != 0]
    
    #joint_cluster = current_data[:, 0] + current_data[:, 1] +current_data[:, 2]
    joint_cluster = current_data[:, 0] + current_data[:, 1] 
    #joint_cluster = current_data[:, 2]

    
    X = np.array([[x] for x in joint_cluster])
    X_plot = np.linspace(-1, 5, int(n))[:, np.newaxis]

    #bins = np.linspace(X.min(), X.max(), 100)
    
    # Gaussian KDE
    #####bandwidth vakue?!
    kde = KernelDensity(kernel='gaussian', bandwidth= 0.08 ).fit(X)
    log_dens = kde.score_samples(X_plot)
    #plt.xlim([0, 1])
    #plt.ylim([-20,2])
    #plt.plot(X_plot[:, 0], (log_dens))
    #plt.show()
    
    #print(log_dens)
    #print(np.exp(log_dens))
    expon = np.exp(log_dens)
    a = expon
    maxima_indices = np.arange ( len (a) )
    maxima_indices = maxima_indices [ ( np.r_[True, a[1:] > a[:-1]] & np.r_[a[:-1] > a[1:], True]) ]
    print (maxima_indices)
    print( X_plot[maxima_indices, 0] )
    plt.plot(X_plot[maxima_indices],expon[maxima_indices],'go' , alpha = 0.5)
    
    plt.fill(X_plot[:, 0], expon, fc='#AAAAFF')
             
    hist, bins = np.histogram(joint_cluster, int( n / 256  ), range = (0, 1))
    
    widths = np.diff(bins)

    #hist = hist / (runNum)
    hist = hist / len( joint_cluster )
    hist = hist / widths[0]
    #hist [ hist<0.1 ] = 0
    plt.bar(bins[:-1], hist, widths,  color = 'r', linewidth=1, alpha = opacity_num)
    #plt.bar(bins[:-1], hist, widths,  color = 'r')
    #plt.bar(bins[:-1], hist[hist>0], widths,  color = 'r', linewidth=0, alpha = opacity_num/3)
    #plt.fill(X_plot[:, 0], log_dens, fc='#AAAAFF')
    zero_limit_indice = np.argmax(X_plot>0)
    one_limit_indice = np.argmax(X_plot>1)
    """
    ######
    X_plot = X_plot[zero_limit_indice : one_limit_indice]
    log_dens = log_dens[zero_limit_indice : one_limit_indice]
    ######
    
    local_min = log_dens.argmin()
    print("p = ",prange[pindex])
    print(local_min)
    q = np.zeros(len(X_plot))
    q[local_min]+=3
    #plt.fill(X_plot[:, 0], q, fc='#AAAAFB')
    #plt.fill(X_plot[:, 0], np.exp(log_dens), fc='#AAAAFF')
    #plt.plot(X[:, 0], np.zeros(X.shape[0]) - 0.01, '+k')
    print(local_min)
    print ( (X_plot[local_min:]).argmax() )
    #plt.text(-3.5, 0.31, "Gaussian Kernel Density")
    """
    plt.ylim([0,3])
    plt.xlim([0, 1])
    
    plt.ylim([0,3])
    #plt.xlim([0.4, 0.9])
    #plt.ylim([0, 0.5])

    name_string = "$normal$, " + dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
    plt.suptitle(name_string)
    plt.xlabel('$mass$')
    plt.ylabel('$P(m)$')

    name_string = name_string.replace('$','')
    plt.grid()
    plt.savefig(location + name_string+".png")
    plt.show()
    
    
"""    
grid = GridSearchCV(KernelDensity(),
                    {'bandwidth': np.linspace(0.1, 1.0, 2)},
                    cv=20) # 20-fold cross-v
grid.fit(joint_cluster[:, None])
"""