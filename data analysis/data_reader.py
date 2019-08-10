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

#with open('../Results/glue_stuff/heteros/D-sh giant clean email 0.0025.txt') as f:
#with open('../Results/glue_stuff/heteros/conference/DCW-sh clean sociopattern_conference_contact non-coop 0.0100.txt') as f:
#with open( '../Results/giant clean primaryschool.txt 0.145 1407863207-data.txt' ) as f:
#with open( '../Results/glue_stuff/heteros/clean sociopattern_hospital 0.0100.txt' ) as f:

#with open('../Results/glue_stuff/heteros/DCWB-sh giant clean primaryschool 0.0200.txt') as f:    
    
#with open('../Results/glue_stuff/heteros/primary school/giant clean primaryschool non-coop 0.0200.txt') as f:
nindex = rindex = pindex = qindex = 0
#file_dir = "../Results/"
#file_dir = "../Results/glue_stuff/heteros/primaryschool-adjusted/non-coop/"
file_dir = "../Results/glue_stuff/heteros/primaryschool-adjusted/coop/"

#file_dir = "../Results/glue_stuff/heteros/hospital/coop/"

#file_dir = "../Results/glue_stuff/heteros/conference/non-coop/"
#file_dir = "../Results/glue_stuff/heteros/"
#file_dir = "../Results/glue_stuff/heteros/primaryschool-adjusted/"
#file_dir = "../Results/"



#file_name = "agg clean sociopattern_conference_contact.txt  non-coop 01e-05 205545703-data.txt"
#file_name = "agg clean sociopattern_conference_contact.txt 1.00e-05 401874239-data.txt"
#file_name = "agg clean sociopattern_conference_contact.txt  non-coop 01e-05 205545703-data.txt"
#file_name = "Erdos 1.25e-05 413026351-data.txt"
#file_name = "hospital/D-sh clean sociopattern_hospital 0.0100.txt"
#file_name = "SO-sh clean sociopattern_hospital.txt 0.01 1556295241-data.txt"

#file_name = "DCW-sh giant clean primaryschool 0.000250.txt"
#file_name = "giant clean primaryschool 0.000250.txt"
#file_name = "SOU-sh giant clean primaryschool 0.000250.txt"
#file_name = "DCB-sh giant clean primaryschool non-coop 0.000250.txt"

#file_name = "DCB-sh clean sociopattern_conference_contact non-coop 0.0100.txt"
#file_name = "D-sh clean sociopattern_conference_contact non-coop 0.0100.txt"
#file_name = "clean sociopattern_hospital 0.0100.txt"


#file_name = "DCWB-sh clean sociopattern_hospital.txt  non-coop 0.06 1624215451-data.txt"
#file_name = "clean sociopattern_conference_contact.txt 0.06 1395082371-data.txt"
#file_name = "DCB-sh giant clean primaryschool 0.0200.txt"
#file_name = "SOU-sh giant clean primaryschool 0.000250.txt"
#file_name = "SOU-sh giant clean primaryschool 0.000250.txt"

second_dir = ""
second_file_name = ""

with open(file_dir + file_name, 'r') as f:

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

data_type = data_type.replace('_', '')
data_type = data_type.replace('.txt', '')
data_type = data_type.replace('giant ', '')
#data_type = data_type.replace('clean ', '')
if ( 'non-coop' in str(f) ):
    qrange = prange
data = np.array(pd_data)
data = np.array(data).reshape(p_size, q_size, runNum,3)

location = "../Results/"