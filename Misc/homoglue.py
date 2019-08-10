import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import result_classifier

#
#print(next(os.walk("../Results/glue_stuff/raw", topdown=True))[1])
#print (os.listdir( "../Results/glue_stuff/raw/0.0800/" ))
#cleaning the homo directory
for root, dirs, files in os.walk("../Results/glue_stuff/homos", topdown=False):
    #print(files)
    True
print(files)
for file in files:
    os.remove(root+'/'+file)

#intendedR = 0.002
path = "../Results/glue_stuff/raw/"
aberrations = []
intendedRunNum = 50000
i = 0
for root, dirs, files in os.walk(path, topdown=True):    

    if(files):
        #print( root + '/' + files[0] )
        with open(root + '/' + files[0]) as f:
            dis_type=(f.readline())
            data_type=(f.readline())
            dis_type = dis_type.replace('\n','')
            data_type = data_type.replace('\n','')
            
            n_size = int(f.readline())
            p_size = int(f.readline())
            q_size = int(f.readline())
            r_size = int(f.readline())
            
                
            thisFileRunNum = int( f.readline() )
            runNum = thisFileRunNum
            nrange = [ int(f.readline()) for i in range(n_size)]
            prange = [ float(f.readline()) for i in range(p_size)]
            qrange = [ float(f.readline()) for i in range(q_size) ]
            rrange = [ float(f.readline()) for i in range(r_size) ]
            #intendedR = rrange[0]
            #if rrange == [0.01]:
                #print(intendedR)
                #print(rrange)
                #print(file)
            
            this_file_data = pd.read_csv(f)
            pd_data = this_file_data
            
            if( thisFileRunNum != len(this_file_data) ):
                print(files[0])
                print("doesn't match the asserted runNum!")
                os.remove(root + '/' + files[0])
                print(prange)
                aberrations.append( prange[0] )
            """    
            if( rrange[0] != intendedR ):
                print("r doesn't match.")
                os.remove(root + '/' + files[0])
                print("r = " + str(rrange[0]))
            """

            
            file_name , _ , _ = files[0].split('.txt')
            if( 'non-coop' in files[0] ):
                file_name = file_name + ' non-coop'
            output_file_name =  "../Results/glue_stuff/homos/" + file_name + " " + "{0:.6f}".format(prange[0]) + ".txt"
            for file in files[1:]:
                with open(root + '/' + file) as f:
                    #print(root + '/' + file)
                    dis_type=(f.readline())
                    data_type=(f.readline())
                    dis_type = dis_type.replace('\n','')
                    data_type = data_type.replace('\n','')
                    #print(file)
                    n_size = int(f.readline())
                    p_size = int(f.readline())
                    q_size = int(f.readline())
                    r_size = int(f.readline())
                    
                    thisFileRunNum = int( f.readline() )
                    runNum += thisFileRunNum
                    nrange = [ int(f.readline()) for i in range(n_size)]
                    prange = [ float(f.readline()) for i in range(p_size)]
                    qrange = [ float(f.readline()) for i in range(q_size) ]
                    rrange = [ float(f.readline()) for i in range(r_size) ]
                    
                    this_file_data = pd.read_csv(f)
                    pd_data = pd_data.append ( this_file_data )
                    #print(file)
                    #print(len(this_file_data))
                    if( thisFileRunNum != len(this_file_data) ):
                        print(file)
                        print("doesn't match the asserted runNum!")
                        os.remove(root + '/' + file)
                        print(prange)
                    """
                    if( rrange[0] != intendedR ):
                        print("r doesn't match.")
                        os.remove(root + '/' + file)
                        print("r = " + str(rrange[0]))
                    """

                    
                    #print(prange)
                    #print( len( pd_data ) )
        np_data = np.array(pd_data)
        #print(prange[0])
        #if( runNum != len(pd_data) ):
            #print(file)
            #print("doesn't match the asserted runNum!")
            #print(prange)
        if( runNum != intendedRunNum ):
            print("ALARM!")
            print(prange)
            print(runNum)
            aberrations.append( prange[0] )
        #print(rrange[0])
        #if( rrange[0] != 0.0):
        #if(True):
            #print("r doesn't match.")
            #print(file)
            #os.remove(root + '/' + file)
            #print("r = " + str(rrange[0]))
        #content = pd_data.to_csv( output_file_name, header = None , index = None , sep = '\t' )
        content = pd_data.to_csv( None, header = None , index = None , sep = ',' )
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
            f.write( str(prange[0]) +'\n' )
            f.write( str(qrange[0]) +'\n' )
            f.write( str(rrange[0]) +'\n' )
            f.write( "ab_cluster, a_cluster, b_cluster\n" )
            f.write(content)

                
            #print(prange)

    #for file in files:
        #print(file)
    #print("done")
    #True
    
"""
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
            output_file_name =  "../Results/glue_stuff/homos/" + str(prange[0]) + ".txt"
            #print(dis_type)

for file in files[1:]:
    with open(root + '/' + file) as f:
            dis_type=(f.readline())
            data_type=(f.readline())
            dis_type = dis_type.replace('\n','')
            data_type = data_type.replace('\n','')
            
            n_size = int(f.readline())
            p_size = int(f.readline())
            q_size = int(f.readline())
            r_size = int(f.readline())
            
                
            runNum += int(f.readline())
            nrange = [ int(f.readline()) for i in range(n_size)]
            prange = [ float(f.readline()) for i in range(p_size)]
            qrange = [ float(f.readline()) for i in range(q_size) ]
            rrange = [ float(f.readline()) for i in range(r_size) ]
            
            
            pd_data = pd_data.append (pd.read_csv(f))
            print( len( pd_data ) )

np_data = np.array(pd_data)

#content = pd_data.to_csv( output_file_name, header = None , index = None , sep = '\t' )
content = pd_data.to_csv( None, header = None , index = None , sep = ',' )

#"""
"""
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
    f.write( str(prange[0]) +'\n' )
    f.write( str(qrange[0]) +'\n' )
    f.write( str(rrange[0]) +'\n' )
    f.write( "ab_cluster, a_cluster, b_cluster\n" )
    f.write(content)
#"""
print(np.sort( aberrations ))
