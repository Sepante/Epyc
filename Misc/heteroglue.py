import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import homoglue

for root, dirs, files in os.walk("../Results/glue_stuff/homos", topdown=False):
    True
files.sort()

with open(root + '/' + files[0]) as f:
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
            output_file_name =  "../Results/glue_stuff/heteros/" + files[0].replace("glued.txt","zuper.txt")
            #print(dis_type)
#"""
for file in files[1:]:
    with open(root + '/' + file) as f:
            #print(f)
            dis_type=(f.readline())
            data_type=(f.readline())
            dis_type = dis_type.replace('\n','')
            data_type = data_type.replace('\n','')
            
            n_size = int(f.readline())
            current_p_size = int (f.readline())
            p_size += current_p_size
            q_size = int(f.readline())
            r_size = int(f.readline())
            
                
            runNum = int(f.readline())
            nrange = [ int(f.readline()) for i in range(n_size)]
            #prange = [ float(f.readline()) for i in range(p_size)]
            #prange = [ float(f.readline()) for i in range(1)]
            for i in range(current_p_size):
                prange.append( float(f.readline()) )
            qrange = [ float(f.readline()) for i in range(q_size) ]
            rrange = [ float(f.readline()) for i in range(r_size) ]
            
            pd_data = pd_data.append (pd.read_csv(f))


np_data = np.array(pd_data)


#content = pd_data.to_csv( output_file_name, header = None , index = None , sep = '\t' )
content = pd_data.to_csv( None, header = None , index = None , sep = ',' )
#"""

#"""
with open(output_file_name, 'w') as f:
    #content = f.read()
    #f.seek(0, 0)
    f.write(dis_type+'\n')
    f.write(data_type+'\n')
    
    f.write( str(n_size) +'\n' )
    f.write( str(p_size) +'\n' )
    f.write( str(q_size) +'\n' )
    f.write( str(r_size) +'\n' )
    f.write( str(runNum) +'\n' )
    
    f.write( str(nrange[0]) +'\n' )
    for p in prange:
        f.write( str(p) +'\n' )
    f.write( str(qrange[0]) +'\n' )
    f.write( str(rrange[0]) +'\n' )
    f.write( "ab_cluster, a_cluster, b_cluster\n" )
    f.write(content)
print(output_file_name)
#"""
