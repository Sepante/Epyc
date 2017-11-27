import numpy as np
import matplotlib.pyplot as plt
#this function binnes the data, ordinary or log, and can return the width of the bins, for the log situation.
def binned( data, xmin, xmax, binNum, log = False, returnwidth = False):
    if(log):
        if(data==[]):
            return[[],[]]
        
        data = np.log10(data)
        xmax = np.log10(xmax)
        xmin = np.log10(xmin)
    bin_array = np.zeros(binNum)
    binLen = (xmax-xmin)/binNum
    for x in data:
        xbin=int((x-xmin)/binLen)
        if x==xmax:
            xbin-=1
        bin_array[xbin]+=1
    if(log):
        x_axis = 10**np.linspace(xmin, xmax+binLen, num = binNum+1) #we add binLen to xmax in order to get 1 more step, for later use is diff (for finding the width.)
        if(returnwidth == False ):        
            return ( np.array([x_axis[:-1], bin_array]) )
            
        if(returnwidth == True ):
            width=np.diff(x_axis)
            #print len(width)
            return ( np.array([x_axis[:-1], bin_array, width]) )
            
    if(not log):
        return np.array([np.arange(xmin, xmax, binLen) ,bin_array])

opacity_num = 0.5
rindex = 0
for nindex in range(n_size):
    for pindex in range(p_size):
        for qindex in range(q_size):
            n = nrange[nindex]
    
            current_data = data[pindex, qindex, :]
            
            high_a = current_data[:, 1] > 200
            high_b = current_data[:, 2] > 200
            joint_condition = np.logical_and(high_a, high_b)
            joint_cluster = current_data[joint_condition,0]
            #in the case that there are 1 or 0 instances.
            
            if len(joint_cluster) < 2:
                binned_data = [[],[]]

            else:
                binned_data =( binned(joint_cluster, 1, np.max(joint_cluster), 200000, log = True,returnwidth = True ) )
                binned_data[1] /= (runNum) #normalizing the bin numbers to one to create the probabiltly.
                binned_data[1] /= (binned_data[2]+1) #changing the probabilty distribution to the probability density.

            #plt.bar(binned_data[0], binned_data[1], binned_data[2])
            plt.plot(binned_data[0], binned_data[1] , color = 'r', alpha = opacity_num )
            #plt.bar(binned_data[0], binned_data[1]/n, binned_data[2])
            #plt.bar(binned_data[0], binned_data[1], wi
            single_cluster = current_data[ np.logical_not(joint_condition) , 0]
            if len(joint_cluster) < 2:
                binned_data = [[],[]]

            else:
                binned_data =( binned(single_cluster, 1, np.max(joint_cluster), 200000, log = True,returnwidth = True ) )
                binned_data[1] /= (runNum) #normalizing the bin numbers to one to create the probabiltly.
                binned_data[1] /= (binned_data[2]+1) #changing the probabilty distribution to the probability density.

            plt.plot(binned_data[0], binned_data[1] , color = 'b', alpha = opacity_num )
            #data_type = " $Primary$ $School: $"
            dis_type = dis_type.replace('\n','')
            data_type = data_type.replace('\n','')
            name_string = dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
            plt.suptitle(name_string)
            plt.xlabel('$mass$')
            plt.ylabel('$P(m)$')
            plt.gca().set_xscale("log")
            plt.gca().set_yscale("log")
            location = "results/"
            name_string = name_string.replace('$','') + "noco"
            plt.savefig(location+name_string+".png")
        
            plt.show()
        

    
    #plt.ylim([0,10000])
    #plt.plot(Q[0],Q[1])
    #plt.gca().set_xscale("log")
    #plt.gca().set_yscale("log")
    
#"""

    """
    #in this part we found the slope of the bins in the left part of the plot.
    
    cons = 100000 #cons is the largest value of x which the linear behaviour on the loglog plot continues. also depends on the number of the bins (binNum).
    x = binned_data[0,:cons]
    y = binned_data[1,:cons]
    
    non_zeros_ind = y != 0
    x = x[non_zeros_ind]
    y = y[non_zeros_ind]
    
    #logx = x[zeros_ind]
    #logy = y[zeros_ind]
    logx = np.log10(x)
    logy = np.log10(y)
    coeffs = np.polyfit(logx,logy,deg=1)
    
    
    plt.plot( x, 10**coeffs[1]*(x**coeffs[0]) ,'r-o')
    
    #plt.bar(binned_data[0,:cons], binned_data[1,:cons], binned_data[2,:cons])
    plt.plot(binned_data[0,:cons], binned_data[1,:cons])
    plt.suptitle("$Erdos$, $p= %.2f$, $q= %.1f$ , $r= %.2f$, $N= %d$, $m= %3f$"%(prange[0],qrange[0],rrange[0],n,coeffs[0]))

    plt.gca().set_xscale("log")
    plt.gca().set_yscale("log")
    plt.show()
    """