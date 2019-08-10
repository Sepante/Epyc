import time

import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler

from scipy.stats import spearmanr as spearmanr

from sklearn.metrics import pairwise_distances
from sklearn import metrics

import os


scatter_plot = False
distances_plot = False
store_on_file = False
#np.random.seed(0)
#X1 = pd_data[['a','run']].groupby('run').max()
#X2 = pd_data[['ab','run']].groupby('run').max()
#X1 = np.array(X1).ravel()
#X2 = np.array(X2).ravel()


pindex = -1
X1 = data[pindex, -1, ::1, 0]
X2 = data[pindex, -1, ::1, 1]

pStep = 1

#tempIndicies = range( len(data) )[::pStep]

tempdata = data[::pStep, -1]
tempprange = prange[::pStep]

distances = np.zeros( len(tempdata) )
max_centers = np.zeros( len(tempdata) )
max_center_sizes = np.zeros( len(tempdata) )

instance_step = 10

for ptempindex, p in enumerate( tempprange ):
    
    X1 = tempdata[ptempindex, ::instance_step, 0]
    X2 = tempdata[ptempindex, ::instance_step, 1]
    
    origX = np.zeros((len(X1), 2), float)
    origX[:, 0] = X1
    origX[:, 1] = X2
    
    # Generate datasets. We choose the size big enough to see the scalability
    # of the algorithms, but not too big to avoid too long running times
    """
    n_samples = 1   
    noisy_circles = datasets.make_circles(n_samples=n_samples, factor=.5,
                                          noise=.05)
    noisy_moons = datasets.make_moons(n_samples=n_samples, noise=.05)
    blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
    no_structure = np.random.rand(n_samples, 2), None
    """
    colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
    colors = np.hstack([colors] * 20)
    
    clustering_names = [
        'MiniBatchKMeans', 'AffinityPropagation', 'MeanShift',
        'SpectralClustering', 'Ward', 'AgglomerativeClustering',
        'DBSCAN', 'Birch']
    
    #clustering_names = ['DBSCAN', 'miniBatch']
    clustering_names = ['KMeans']
    if scatter_plot:
        plt.figure(figsize=(len(clustering_names) * 2 + 3, 9.5))
        plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05,
                            hspace=.01)
    
        plot_num = 1
    
    #datasets = [noisy_circles, noisy_moons, blobs, no_structure]
    datasets = ['temp']
    
    for i_dataset, dataset in enumerate(datasets):
        #X, y = dataset
        # normalize dataset for easier parameter selection
        scaler = StandardScaler().fit(origX)
        X = scaler.fit_transform(origX)

        KMeans = cluster.KMeans(n_clusters=3)

        #dbscan = cluster.DBSCAN(eps=0.0885)

        #clustering_algorithms = [dbscan, KMeans]
        clustering_algorithms = [KMeans]
    
        for name, algorithm in zip(clustering_names, clustering_algorithms):
            # predict cluster memberships
            t0 = time.time()
            algorithm.fit(X)
            t1 = time.time()
            if hasattr(algorithm, 'labels_'):
                y_pred = algorithm.labels_.astype(np.int)
            else:
                y_pred = algorithm.predict(X)
            
            qtext = str(qrange[qindex])
            if ( 'non-coop' in str(f) ):
                qtext = 'p'

            if scatter_plot:
                # plot
                plt.subplot(3, len(clustering_algorithms), plot_num)
                #if i_dataset == 0:
                    
        
                name_string = name+"clustering for $a$ and $ab$ values, \n"+ dis_type + ", " + data_type + "\n" +", $n=$" + str(nrange[nindex]) + ", $p=$" + str( p )+ ", $q=$" + qtext + ", $r=$" + str(rrange[rindex])
                plt.title(name_string)
                plt.scatter(origX[:, 0], origX[:, 1], color=colors[y_pred].tolist(), s=25, alpha = 0.1)
                #plt.ylim([0, 75])
                #plt.ylim([0, 75])
                #plt.scatter(X1, X2, color=colors[y_pred].tolist(), s=10, alpha = 0.2)
                
                plt.xlabel('$ a( \infty$ )')
                plt.ylabel('$ ab( \infty$ )')
        
                plot_num += 1
    if scatter_plot:
        plt.savefig(location+"clustering/"+name_string+".png" , dpi = 300, bbox_inches='tight')
        plt.show()
    centers = ( scaler.inverse_transform( KMeans.cluster_centers_  ))
    max_center_id = centers[:,0].argmax()
    max_center = centers[ max_center_id ]
    max_center_size = np.sum(y_pred == max_center_id) / runNum
    non_max_center = origX[y_pred != max_center_id].mean(0)
    #centers = np.array([ origX[y_pred == 0].mean(0), origX[y_pred == 1].mean(0), origX[y_pred == 2].mean(0) ])
    #distance = np.linalg.norm( centers[0]-centers[1] ) + np.linalg.norm( centers[1]-centers[2] ) + np.linalg.norm( centers[0]-centers[2] )
    
    centers_distance = np.linalg.norm( max_center - non_max_center )
    
    max_center_sizes[ptempindex] = max_center_size
    max_centers[ptempindex] = max_center[0]
    distances[ptempindex] = centers_distance
    #print (distance)
    
    
    #print( metrics.silhouette_score(X, y_pred, metric='euclidean') )
    #print ( metrics.calinski_harabasz_score(X, y_pred)   )
    """
    y_values = np.sort ( list ( set(y_pred) ) )
    y_values = y_values[ y_values >= 0 ]
    for y in  y_values:
        print(y)
        print( X[ y_pred == y , 1].mean() )
        
    #"""
    plot_corr = 0
    
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
        ", $n=$" + str(nrange[nindex]) + ", $p=$" + str( p )\
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
if distances_plot:
    """
    plt.plot( tempprange, distances, '--o' )
    name_string = dis_type + ", " + data_type + "\n" +\
    ", $n=$" + str(nrange[nindex]) +\
    ", $q=$" + qtext + ", $r=$" + str(rrange[rindex])

    plt.title(name_string)
    plt.xlabel('$p$')
    plt.ylabel('Sum of pair-wise distances')
    plt.show()
    """
    plt.plot( tempprange, max_centers/nrange[nindex], '--o' )
    name_string = dis_type + ", " + data_type + "\n" +\
    ", $n=$" + str(nrange[nindex]) +\
    ", $q=$" + qtext + ", $r=$" + str(rrange[rindex])

    plt.title(name_string)
    plt.xlabel('$p$')
    plt.ylabel('average of $ab$ for giant cluster')
    plt.show()

    
    plt.plot( tempprange, max_center_sizes, '--ro' )
    name_string = dis_type + ", " + data_type + "\n" +\
    ", $n=$" + str(nrange[nindex]) +\
    ", $q=$" + qtext + ", $r=$" + str(rrange[rindex])

    plt.title(name_string)
    plt.xlabel('$p$')
    plt.ylabel('Outbreak Probability')
    plt.show()




if store_on_file:
    shuffle_type , file_name = data_type.split('clean ') 
    shuffle_type = shuffle_type.replace('$', '')
    shuffle_type = shuffle_type + 'clean'
    file_name = location + "KMeansClustering/" + file_name.replace('$', '') + "giant-cluster-ave.csv"
    tempprange = np.array(tempprange)


    with open(file_name, "a") as f:
        DF = pd.DataFrame([max_centers] , index = [shuffle_type], columns = tempprange)
        file_empty = (os.stat(file_name).st_size == 0)
        if file_empty:
            DF.to_csv(f)
        else:
            DF.to_csv(f, header = False)
    
    
    shuffle_type , file_name = data_type.split('clean ') 
    shuffle_type = shuffle_type.replace('$', '')
    shuffle_type = shuffle_type + 'clean'
    file_name = location + "KMeansClustering/" + file_name.replace('$', '') + "giant-cluster-instances.csv"
    tempprange = np.array(tempprange)
    
    
    
    
    with open(file_name, "a") as f:
        DF = pd.DataFrame([max_center_sizes] , index = [shuffle_type], columns = tempprange)
        file_empty = (os.stat(file_name).st_size == 0)
        if file_empty:
            DF.to_csv(f)
        else:
            DF.to_csv(f, header = False)


shuffle_type , file_name = data_type.split('clean ') 
shuffle_type = shuffle_type.replace('$', '')
shuffle_type = shuffle_type + 'clean'
file_name = location + "KMeansClustering/" + file_name.replace('$', '') + "outbreakP.csv"
#with open(file_name, "a") as f:
with open(file_name, "a") as f:
    DF = pd.DataFrame([distances] , index = [shuffle_type], columns = tempprange)
    file_empty = (os.stat(file_name).st_size == 0)
    if file_empty:
        DF.to_csv(f)
    else:
        DF.to_csv(f, header = False)

