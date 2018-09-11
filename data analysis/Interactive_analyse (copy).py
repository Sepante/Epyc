import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal

'''
Lognorm: Instead of pcolor log10(Z1) you can have colorbars that have
the exponential labels using a norm.
'''
#N = 11
#X1, Y1 = np.mgrid[-3:3:complex(0, N), -2:2:complex(0, N)]
X, Y = np.meshgrid( np.array(prange) , np.arange( binNum + 1) )

#Z1 = np.random.uniform(0, 10, (N, N) )


fig, ax = plt.subplots(2, 1)

#pcm = ax[0].pcolor(X, Y, hist.T,
pcm = ax[0].pcolor(,
                   #norm=colors.LogNorm(vmin=hist.min()+ 3, vmax=hist.max()),
                   norm=colors.PowerNorm(gamma = 0.30 ),
                   #cmap='PuBu_r'
                   cmap=plt.cm.Blues
                   
                   )
fig.colorbar(pcm, ax=ax[0], extend='max')
qhist = hist
#qhist [ qhist > 0 ] = 1
ax[0].set_yscale('log')
ax[0].xlim([10,20])
pcm = ax[1].pcolor(X, Y, qhist.T
        #, cmap='PuBu_r'
        , cmap=plt.cm.Blues
        )
fig.colorbar(pcm, ax=ax[1], extend='max')
#fig.show()
