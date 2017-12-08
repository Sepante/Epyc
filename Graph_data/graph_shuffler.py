import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as rd


pd_data = pd.read_csv('clean_input_matrix.txt', sep ='\t', header = None)
temp_graph = np.array(pd_data)
temp_graph_stable = np.copy(temp_graph)



edge_count = pd.Series(temp_graph[:, 0])
edge_count = edge_count.value_counts()
edge_count = edge_count.sort_index()
edge_count = np.array(edge_count.reset_index())
#"""
#c_grain_size = len(temp_graph)
c_grain_size = 100
splitted_edge = np.array_split(edge_count[:,1],c_grain_size)
splitted_time = np.array_split(edge_count[:,0],c_grain_size)
c_grained_count_edge = [np.mean(inst) for inst in splitted_edge]
c_grained_count_time = [np.mean(inst) for inst in splitted_time]

plt.plot(c_grained_count_time, c_grained_count_edge, '-o')
#"""


#pd_data.to_csv('new_mat.txt',index = False, header = False, sep = '\t', columns=[1,2])
np.random.shuffle(temp_graph)
#"""
j = 0
for i in range(len(temp_graph)):
    temp_graph[i, 0] = j * 20
    if (i % 40 == 39):
        print(i)
        j += 1
#"""
t_ave_graph = pd.DataFrame(temp_graph)
t_ave_graph.to_csv('t_ave_graph.txt',index = False, header = False, sep = '\t')

temp_graph[:, 0] = temp_graph_stable[:, 0]
t_respect_graph = pd.DataFrame(temp_graph)
t_respect_graph.to_csv('t_respect_graph.txt',index = False, header = False, sep = '\t')