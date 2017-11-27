import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from pylab import *



with open('grid_visualize.csv') as f:
    pn_data = pd.read_csv(f, index_col = False, header = None)


vis_data = np.array(pn_data)
l = len(vis_data[0])
t = int(len(vis_data) / l)

vis_data = np.array(vis_data).reshape(t, l, l)
bounds = np.array([0, 1, 2, 3, 4, 6, 9, 12, 18, 36]) + 0.1
cmap = mpl.colors.ListedColormap(['royalblue', 'pink', 'pink' ,'orange', 'red', 'yellow', 'pink', 'pink', 'green'])
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

images = []
location = "results/grid_animation/"
for t, anim_step in enumerate(vis_data):
    imshow(anim_step, cmap = cmap, norm = norm, interpolation='nearest')
    #grid(True)
    name_string = '{:003d}'.format(t)
    plt.suptitle(name_string)
    if t%5 == 4:
        plt.savefig(location+name_string+".png")
    
    #plt.show(fig)
    #plt.show()
