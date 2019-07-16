#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 16:30:23 2019

@author: sina sajjadi
"""


import time

import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler

from scipy.stats import spearmanr as spearmanr

#np.random.seed(0)

X1 = pd_data[['a','run']].groupby('run').max()
X2 = pd_data[['ab','run']].groupby('run').max()
X1 = np.array(X1).ravel()
X2 = np.array(X2).ravel()

#X1 = current_data[pindex, ::4, 0]
#X2 = current_data[pindex, ::4, 1]

#X2 = X2 + X1

X = np.zeros((len(X1), 2), float)
X[:, 0] = X1
X[:, 1] = X2

# Generate datasets. We choose the size big enough to see the scalability
# of the algorithms, but not too big to avoid too long running times
n_samples = 1   
noisy_circles = datasets.make_circles(n_samples=n_samples, factor=.5,
                                      noise=.05)
noisy_moons = datasets.make_moons(n_samples=n_samples, noise=.05)
blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
no_structure = np.random.rand(n_samples, 2), None

colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
colors = np.hstack([colors] * 20)

clustering_names = [
    'MiniBatchKMeans', 'AffinityPropagation', 'MeanShift',
    'SpectralClustering', 'Ward', 'AgglomerativeClustering',
    'DBSCAN', 'Birch']

clustering_names = ['DBSCAN']

plt.figure(figsize=(len(clustering_names) * 2 + 3, 9.5))
plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05,
                    hspace=.01)

plot_num = 1

datasets = [noisy_circles, noisy_moons, blobs, no_structure]
datasets = ['temp']

for i_dataset, dataset in enumerate(datasets):
    #X, y = dataset
    # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)
    #X[:,0] *= 2
    # estimate bandwidth for mean shift
    """
    bandwidth = cluster.estimate_bandwidth(X, quantile=0.3)

    # connectivity matrix for structured Ward
    connectivity = kneighbors_graph(X, n_neighbors=10, include_self=False)
    # make connectivity symmetric
    connectivity = 0.5 * (connectivity + connectivity.T)

    # create clustering estimators
    ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
    two_means = cluster.MiniBatchKMeans(n_clusters=2)
    ward = cluster.AgglomerativeClustering(n_clusters=2, linkage='ward',
                                           connectivity=connectivity)
    spectral = cluster.SpectralClustering(n_clusters=2,
                                          eigen_solver='arpack',
                                          affinity="nearest_neighbors")
    """
    #dbscan = cluster.DBSCAN(eps=0.089)
    dbscan = cluster.DBSCAN(eps=0.7)
    #dbscan = cluster.DBSCAN(eps=0.096)
    """
    affinity_propagation = cluster.AffinityPropagation(damping=.9,
                                                       preference=-200)

    average_linkage = cluster.AgglomerativeClustering(
        linkage="average", affinity="cityblock", n_clusters=2,
        connectivity=connectivity)

    birch = cluster.Birch(n_clusters=2)
    
    clustering_algorithms = [
        two_means, affinity_propagation, ms, spectral, ward, average_linkage,
        dbscan, birch]
    """

    #clustering_names = [clustering_names[-2]]
    clustering_algorithms = [dbscan]

    for name, algorithm in zip(clustering_names, clustering_algorithms):
        # predict cluster memberships
        t0 = time.time()
        algorithm.fit(X)
        t1 = time.time()
        if hasattr(algorithm, 'labels_'):
            y_pred = algorithm.labels_.astype(np.int)
        else:
            y_pred = algorithm.predict(X)

        # plot
        plt.subplot(3, len(clustering_algorithms), plot_num)
        if i_dataset == 0:
            
            qtext = str(qrange[qindex])
            if ( 'non-coop' in str(f) ):
                qtext = 'p'

            name_string = "DBSCAN clustering for $a$ and $ab$ values, \n"+ dis_type + ", " + data_type + "\n" +", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex])+ ", $q=$" + qtext + ", $r=$" + str(rrange[rindex])
            plt.title(name_string)
        plt.scatter(X[:, 0], X[:, 1], color=colors[y_pred].tolist(), s=15, alpha = 0.2)
        #plt.scatter(X1, X2, color=colors[y_pred].tolist(), s=10, alpha = 0.2)
        
        plt.xlabel('$scaled$ $ a( \infty$ )')
        plt.ylabel('$scaled$ $ ab( \infty$ )')

        """
        if hasattr(algorithm, 'cluster_centers_'):
            centers = algorithm.cluster_centers_
            center_colors = colors[:len(centers)]
            plt.scatter(centers[:, 0], centers[:, 1], s=100, c=center_colors, alpha = 0.5)
        """
        #plt.xlim(-1.1, 2)
        #plt.ylim(-1.1, 2)
        #plt.xticks(())
        #plt.yticks(())
        #plt.text(.99, .01, ('%.2fs' % (t1 - t0)).lstrip('0'),
                 #transform=plt.gca().transAxes, size=15,
                 #horizontalalignment='right')
        plot_num += 1

plt.savefig(location+"clustering/"+name_string+".png" , dpi = 300, bbox_inches='tight')
plt.show()

"""
y_values = np.sort ( list ( set(y_pred) ) )
y_values = y_values[ y_values >= 0 ]
for y in  y_values:
    print(y)
    print( X[ y_pred == y , 1].mean() )
    
#"""
plot_corr = 1

if plot_corr:
    corrs = []
    spearcorr = []
    giant_cluster = np.where(y_pred == 1)[0]
    giant_cluster_data = pd_data [ pd_data.run.isin( giant_cluster ) ]
    for run in giant_cluster:
        AB_array = giant_cluster_data[giant_cluster_data['run'] == run]['AB']
        A_array  = giant_cluster_data[giant_cluster_data['run'] == run]['A']
        corrs.append( np.corrcoef( AB_array, A_array )[0,1] )
        spearcorr.append( spearmanr( AB_array, A_array )[0] )
        #print(np.corrcoef( AB_array, A_array )[0,1])
    #hist, bins = np.histogram(corrs,20)
    #widths = np.diff(bins)
    #hist = hist / (runNum)
    #hist = hist / widths[0]
    #plt.bar(bins[:-1], hist, widths,  color = 'g', alpha = 1, ec='black')
    plt.hist(corrs, 15, color = 'orange', ec='black')
    
    name_string = "distribution of $A$ and $AB$ correlation over time \n for each, unfiltered realization"\
    + dis_type + ", " + data_type + "\n" +\
    ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex])\
    + ", $q=$" + qtext + ", $r=$" + str(rrange[rindex])
    plt.title(name_string)
    plt.xlabel('$A-AB$ correlation')
    plt.ylabel('$P(A-AB$ correlation)')
    plt.savefig( location+"clustering/"+name_string+".png" , dpi = 300, bbox_inches='tight' )
    plt.show()
    
    #plt.hist(spearcorr)
    #plt.show()

    """
    corrs = []
    for run in range(runNum):
        AB_array = pd_data[pd_data['run'] == run]['AB']
        A_array  = pd_data[pd_data['run'] == run]['A']
        corrs.append( np.corrcoef( AB_array, A_array )[0,1] )
        #print(np.corrcoef( AB_array, A_array )[0,1])
    #hist, bins = np.histogram(corrs,20)
    #widths = np.diff(bins)
    #hist = hist / (runNum)
    #hist = hist / widths[0]
    #plt.bar(bins[:-1], hist, widths,  color = 'g', alpha = 1, ec='black')
    plt.hist(corrs, 20, color = 'orange', ec='black')
    plt.show()
    #"""