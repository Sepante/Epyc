from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
#this function binnes the data, ordinary or log, and can return the width of the bins, for the log situation.
def binned( data, xmin, xmax, binNum, log = False, returnwidth = False):
    if(log):
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
#"""
##########################

#with open('cdata.txt') as f:
with open('cdata.txt') as f:
    #for i in range(1):
    dis_type=(f.readline())
    data_type=(f.readline())
    
    data=[float(i) for i in f]


n_size = int(data.pop(0))
#n = int(data.pop(0))
p_size = int(data.pop(0))
q_size = int(data.pop(0))
r_size = int(data.pop(0))
runNum = int(data.pop(0))
nrange = [ int(data.pop(0)) for i in range(n_size)]
prange = [ data.pop(0) for i in range(p_size)]
qrange = [ data.pop(0) for i in range(q_size)]
rrange = [ data.pop(0) for i in range(r_size)]

data =( np.array(data) )

data =( np.array(data).reshape(p_size, q_size, runNum) )
#"""
#for nindex in [7]:
rindex = 0
for nindex in range(n_size):
    for pindex in range(p_size):
        for qindex in range(q_size):
            #plt.plot(prange, data[:,qindex,:],'o' , color='g', alpha=opacity_num )
            current_data = data[pindex, qindex, :]
    
            n = nrange[nindex]
            #current_data = data[nindex*runNum : (nindex+1)*runNum]
            #current_data = data[nindex*runNum : (nindex+1)*runNum]
            binned_data =( binned(current_data, 1, np.max(current_data), 200000, log = True,returnwidth = True ) )
            binned_data[1] /= (runNum) #normalizing the bin numbers to one to create the probabiltly.
            binned_data[1] /= (binned_data[2]+1) #changing the probabilty distribution to the probability density.
            
            #plt.bar(binned_data[0], binned_data[1], binned_data[2])
            plt.plot(binned_data[0], binned_data[1] )
            #plt.bar(binned_data[0], binned_data[1]/n, binned_data[2])
            #plt.bar(binned_data[0], binned_data[1], wi
            
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
            name_string = name_string.replace('$','')
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