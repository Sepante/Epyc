import matplotlib.pyplot as plt
import numpy as np
import pandas as pd    
from pylab import *


with open('grid_visualize.csv') as f:
    pn_data = pd.read_csv(f, index_col = False, header = None)


vis_data = np.array(pn_data)
l = len(vis_data[0])
t = int(len(vis_data) / l)

vis_data = np.array(vis_data).reshape(t, l, l)

#imshow(A, interpolation='nearest')

for time_step in vis_data:
    #plt.matshow(time_step)
    imshow(time_step, interpolation='nearest')
    #grid(True)
    plt.show()
