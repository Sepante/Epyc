import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

with open('cdata.txt') as f:
    dis_type=(f.readline())
    data_type=(f.readline())
    
    n_size = int(f.readline())
    p_size = int(f.readline())
    q_size = int(f.readline())
    r_size = int(f.readline())
    
        
    runNum = int(f.readline())
    nrange = [ int(f.readline()) for i in range(n_size)]
    prange = [ float(f.readline()) for i in range(p_size)]
    qrange = [ float(f.readline()) for i in range(q_size) ]
    rrange = [ float(f.readline()) for i in range(r_size) ]
    
    
    pd_data = pd.read_csv(f)

data = np.array(pd_data)
data = np.array(data).reshape(p_size, q_size, runNum,3)
nindex = rindex = pindex = 0
