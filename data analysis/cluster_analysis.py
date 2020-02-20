import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from sklearn import cluster, datasets
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler

from scipy.stats import spearmanr as spearmanr

from sklearn.metrics import pairwise_distances
from sklearn import metrics

import os
import pandas as pd



non_coop = True

location = "../Results/"
FullLoc = location + "KMeansClustering/"

#dataType = "sociopatternhospital"
#dataType = "sociopatternconferencecontact"

dataType = "primaryschool"

matplotlib.rcParams.update({'font.size': 15})

fig = plt.figure()
ax = fig.add_subplot(1,1,1)


cooperativity = ''
if non_coop:
    cooperativity = 'non-coop-'


file_name = FullLoc + cooperativity + dataType + "giant-cluster-ave.csv"




print(file_name)

with open(file_name) as f:
    KMeanResults = pd.read_csv(f, index_col = 0)
    #KMeanResults = KMeanResults.transpose()
prange = [ float(p) for p in KMeanResults.columns  ]    
for i in range( len(KMeanResults) ):
    label = KMeanResults.iloc[i].name

    label = label.replace(' clean','')
    label = label.replace(' giant','')
    label = label.replace('giant ','')
    if(label == 'clean'):
        label = 'original'

    ax.plot(prange , KMeanResults.iloc[i], '--o', label = label, alpha = 0.8)
    

ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
ax.yaxis.major.formatter._useMathText = True


ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
ax.xaxis.major.formatter._useMathText = True

ax.get_yaxis().get_offset_text().set_position((-0.15,0))

ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
ax.set_xlabel('$p$')
#plt.ylabel('$giant$ $cluster$ $ab$, $mean$')
ax.set_ylabel( '$\\widebar{ab}$' )
ax.set_xlim(0.003, prange[-1])
#ax.set_xlim(0.02, 0.069)
ax.grid()
fig.savefig(FullLoc + cooperativity + dataType.replace('.txt','') + "giantclusterabmean.png" , dpi = 300, bbox_inches='tight')
#fig.show()
plt.show()

fig2 = plt.figure()
ax = fig2.add_subplot(1,1,1)

file_name = FullLoc + cooperativity + dataType +"giant-cluster-instances.csv"

print(file_name)


with open(file_name) as f:
    KMeanResults = pd.read_csv(f, index_col = 0)
    #KMeanResults = KMeanResults.transpose()
prange = [ float(p) for p in KMeanResults.columns  ]

for i in range( len(KMeanResults) ):
    label = KMeanResults.iloc[i].name 
    
    label = label.replace(' clean','')
    label = label.replace(' giant','')
    label = label.replace('giant ','')
    if(label == 'clean'):
        label = 'original'
    
    ax.plot(prange , KMeanResults.iloc[i], '--*', label = label, alpha = 0.8)
    

ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
ax.yaxis.major.formatter._useMathText = True

ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
ax.xaxis.major.formatter._useMathText = True

ax.get_yaxis().get_offset_text().set_position((-0.15,0))
#ax.get_yaxis().get_label().set_position((-1000,0.5))

ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
ax.set_xlabel('$p$')
#plt.ylabel('$outbreak$ $probability$')
ax.set_ylabel('$P_{ab}$')
ax.set_xlim(0.003, prange[-1])
#ax.set_xlim(0.02, 0.069)

ax.grid()

fig2.savefig(FullLoc + cooperativity + dataType.replace('.txt','') + "outbreakprobability.png" , dpi = 300, bbox_inches='tight')
#plt.show()