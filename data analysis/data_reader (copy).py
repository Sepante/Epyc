import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax

data = np.random.normal(loc=100,scale=10,size=(500,1,32))
hist = np.ones((32,20)) # initialise hist
for z in range(32):
    hist[z],edges = np.histogram(data[:,0,z],bins=np.arange(80,122,2))

ticks = np.linspace(0,20,5)
ax.Ax.set_xticks(ticks)
plt.imshow(hist,cmap='Reds')
