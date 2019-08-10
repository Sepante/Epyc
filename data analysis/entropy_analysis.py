import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
location = "../Results/"
FullLoc = location + "crossEntropy/"


file_name = FullLoc + "totalCrossEntropy.csv"
with open(file_name) as f:
    KMeanResults = pd.read_csv(f, index_col = 0)
    #KMeanResults = KMeanResults.transpose()

x = range( len(KMeanResults.columns) )
shuffle_labels = KMeanResults.columns
plt.xticks(x, shuffle_labels)

for i in range( len(KMeanResults) ):
    label = KMeanResults.iloc[i].name 
    plt.plot(KMeanResults.iloc[i], '--^', label = label)
    
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
#plt.xlabel('$p$')
plt.ylabel('$Cross$ $Entropy$ $with$ $the$ $original$ $network$')
plt.grid()
plt.savefig(FullLoc + "CrossEntropy.png" , dpi = 300, bbox_inches='tight')
plt.show()
