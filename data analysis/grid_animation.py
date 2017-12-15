import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from data_reader import *
from pylab import *
import time

with open('../Results/grid_visualize.csv') as f:
    pn_data = pd.read_csv(f, index_col = False, header = None)

dis_type = dis_type.replace('\n','')
data_type = data_type.replace('\n','')
p_str = '{0:04.3f}'.format(prange[pindex])
q_str = '{0:04.3f}'.format(qrange[qindex])
#n_str = '{:05d}'.format(nrange[nindex])
n_str = '{:d}'.format(nrange[nindex])
r_str = '{0:04.3f}'.format(rrange[rindex])
name_string = dis_type + ", " + data_type + ", $n=$" + n_str + ", $p=$" + p_str + ", $q=$" + q_str + ", $r=$" + r_str
name_string = name_string.replace('$','')
vis_data = np.array(pn_data)
l = len(vis_data[0])
total_t = int(len(vis_data) / l)

vis_data = np.array(vis_data).reshape(total_t, l, l)
bounds = np.array([0, 1, 2, 3, 4, 6, 9, 12, 18, 36]) + 0.1
cmap = mpl.colors.ListedColormap(['royalblue', 'pink', 'pink' ,'orange', 'red', 'yellow', 'pink', 'pink', 'green'])
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
num_string = '{:04d}'.format(10)

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
#images = []
location += "../Results/grid_animation/"

#for t, anim_step in enumerate(vis_data):
def animate(t):
    fig = imshow(vis_data[t], cmap = cmap, norm = norm, interpolation='nearest')
    #grid(True)
    num_string = '{:04d}'.format(t)
    plt.suptitle(name_string+", step: "+ num_string)
    print(t)
    #if t%1==0:
        #print(t)
        #plt.savefig(location+name_string+", step: "+num_string+".png")
    
    #print(anim_step)
    #plt.show()


ani = animation.FuncAnimation(fig, animate, interval = 60000, save_count = total_t)

dpi = 200
writer = animation.writers['ffmpeg'](fps = 10)
file_name = location + str(time.gmtime()[0:5]) + '.mp4'
ani.save( file_name , writer=writer,dpi=dpi)