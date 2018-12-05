import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#with open('../Results/cdatab.txt') as f:
#with open('../Results/normal clean brazil.txt985-data.txt') as f:
#with open('../Results/normal clean sociopattern_hospital.txt981-data.txt') as f:
#with open('../Results/clean brazil.txt 1037-data.txt') as f:
#with open('../Results/clean brazil.txt -data.txt') as f:
#with open('../Results/clean sociopattern_hospital.txt 373442375-data.txt') as f:


#with open('../Results/glue_stuff/heteros/agg giant clean primaryschool.txt 0.000625 1166116669-data.txt') as f:
    
#with open('../Results/glue_stuff/heteros/giant clean brazil 0.0250.txt') as f:
#with open('../Results/glue_stuff/heteros/DCW-sh clean sociopattern_hospital non-coop 0.0100.txt') as f:
#with open('../Results/glue_stuff/heteros/giant clean brazil 0.0125.txt') as f:
#with open('../Results/glue_stuff/heteros/D-sh giant clean brazil non-coop 0.3000.txt') as f:

with open('../Results/glue_stuff/heteros/D-sh giant clean email 0.0025.txt') as f:
#with open('../Results/glue_stuff/heteros/conference/DCW-sh clean sociopattern_conference_contact non-coop 0.0100.txt') as f:
    
#with open('../Results/glue_stuff/heteros/DCWB-sh giant clean primaryschool 0.0200.txt') as f:    
    
#with open('../Results/glue_stuff/heteros/primary school/giant clean primaryschool non-coop 0.0200.txt') as f:
    


#with open('../Results/bursty grid 0.15.txt 1380287758-data.txt') as f:

    dis_type=(f.readline())
    data_type=(f.readline())
    dis_type = dis_type.replace('\n','')
    data_type = data_type.replace('\n','')
    
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
if ( 'non-coop' in str(f) ):
    qrange = prange
data = np.array(pd_data)
data = np.array(data).reshape(p_size, q_size, runNum,3)
nindex = rindex = pindex = qindex = 0
location = "../Results/sunday/email-seminar/"