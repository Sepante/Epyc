import importlib as im
import numpy as np
import matplotlib.pyplot as plt
import data_reader as data_1
im.reload(data_1)
import scipy.stats as stats
import matplotlib
#import data_reader as data_2

prange = prange[0]

n = data_1.nrange[data_1.nindex]

ab_cluster_display = True
R_cluster_display = True
a_cluster_display = False

opacity_num = 0.5
binLen = 10
binNum = int(n/binLen)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

matplotlib.rcParams.update({'font.size': 15})

def remove_zero(string):
    if string[-2] == '0':
        return string[:-2] + string[-1]
    else:
        return string

hist = np.zeros((data_1.p_size ,binNum), dtype=float)

for qindex in range(data_1.q_size):
    q = data_1.qrange[qindex]
    for pindex in range(data_1.p_size):
    #for pindex in range(1):
        p = data_1.prange[pindex]
        #print (p,q)
        
        current_data = data_1.data[:, qindex, :]
        #joint_cluster = current_data[joint_condition, 0]
        #joint_cluster = np.sum(current_data[joint_condition, :],1)
        """
        if(R_cluster_display):
            R_cluster = np.sum( data[pindex, qindex, :] ,1)
            hist, bins = np.histogram(R_cluster, bins, range = (0, n))
            widths = np.diff(bins)
            hist = hist / (runNum)
            hist = hist / widths[0]
            plt.bar(bins[:-1], hist, widths,  color = 'r', linewidth=0, alpha = opacity_num)
        """
        
        """ still needs some work (I am not sure what it is)
        if(a_cluster_display):
            single_cluster = current_data[joint_condition, 0] - current_data[joint_condition, 2]
            #single_cluster = current_data[ np.logical_not(joint_conditiosingn) , 0]
            hist, bins = np.histogram(single_cluster, bins, range = (0, n))
            widths = np.diff(bins)
            hist = hist / (runNum)
            hist = hist / widths[0]
            plt.bar(bins[:-1], hist, widths,  color = 'g', linewidth=0, alpha = opacity_num)
        """

        #"""
        if(ab_cluster_display):
            #ab_cluster = current_data[pindex,:,1] + current_data[pindex,:,2]
#            ab_cluster = np.sum(current_data[pindex],1) #for SIR-SIR
            #ab_cluster = current_data[pindex,:,0]+current_data[pindex,:,1] #for SIS-SIR (only considering 
            #                                                               the first two columns from the output)
            #ab_cluster = current_data[pindex,:,0] +current_data[pindex,:,1] + current_data[pindex,:,2]
            ab_cluster = current_data[pindex,:,0]
            #ab_cluster = data_1.data[pindex, qindex, :, 0]
            #ab_cluster = np.sum(data_1.data[pindex, qindex, :, :],1)
            #ab_cluster = np.exp(data_1.data[pindex, qindex, :, 0])
            #print(ab_cluster.max())
            #print(len(ab_cluster))
            
            #ab_cluster = ab_cluster[::2]
            #ab_cluster = ab_cluster[y_pred == 0]
            
            hist[pindex], bins = np.histogram(ab_cluster, binNum, range = (0, n))
            #plt.bar(bins[:-1], hist[pindex], widths,  color = 'b', linewidth=0, alpha = opacity_num)            
            #print(hist[pindex].sum())
            #print('\n')
        #"""
        """
        name_string = "$normal$, " + dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
        plt.suptitle(name_string)
        plt.xlabel('$mass$')
        plt.ylabel('$P(m)$')

        name_string = name_string.replace('$','')
        plt.ylim([0,0.05])
        plt.xlim([0,n])
        
        plt.savefig(location+name_string+".png")
        
        """
        
    widths = np.diff(bins)
    hist = hist / (data_1.runNum)
    hist = hist / widths[0]
    
    #hist = hist[:, 10:]
    
    
    #hist [ hist > 0 ] = 1
    #hist %= 0.06 #for now (be careful)
    #hist = hist**(4)
    #lower_limit = 0.00015
    #lower_limit = 0.02
    #hist[hist < lower_limit] = lower_limit
    #upper_limit = 0.052
    #hist[hist > upper_limit] = upper_limit
    #hist *=100
    #"""
    #hist = hist[:, 2:100]
    im1 = hist.T
    #omitted_bins = 20 #primaryschool
    #omitted_bins = 15 #hospital and conference
    omitted_bins = 0
    
    im1 = im1[omitted_bins:]
    
    
    exponent = int ( np.floor(  np.log10( im1.max() / 2 ) )  ) #scientific exponent
    #im1 *= 10 ** -exponent
    #im1 = np.log10( im1 )
    
    
    #ax1.imshow(im1, interpolation='none', aspect = 8, cmap=plt.cm.BuPu_r)
    #fig1.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    #cax = plt.axes([0.85, 0.1, 0.075, 0.8])
    #fig1.colorbar(cax=cax)
    #ax1.set_title('5 X 5')
    #"""
    #"""
    
    #aspect = 0.07 / binNum #hospital
    #aspect = 0.0045 / binNum #primaryschool
    aspect = 0.0025 / binNum #non coop primary
    #plt.subplot(111)
    #cs = ax.imshow(im1, interpolation='none', origin = 'lower', aspect = 50/binNum , cmap=plt.cm.gnuplot)
    cs = ax.imshow(im1, interpolation='none', origin = 'lower', aspect = aspect , cmap=plt.cm.gnuplot , extent =[prange[0],prange[-1],  1 + omitted_bins * binLen ,  n ] )
    #cs = ax.imshow(im1, interpolation='none', origin = 'lower', cmap=plt.cm.gnuplot , extent =[prange[0],prange[-1],  1 + omitted_bins * binLen ,  n ] )
    
    
    #vmin = cs.get_array().min()
    #vmax = cs.get_array().max()
    #norm = colors.Normalize(vmin=vmin, vmax=vmax)

    #cs.set_norm(norm)
    #cs = ax.imshow(im1, interpolation='none', origin = 'lower' , cmap=plt.cm.gnuplot,  extent=[prange[0], prange[-1], 1, n])
    #plt.imshow(im1, interpolation='none', origin = 'lower', aspect = 80/binNum , cmap=plt.cm.gnuplot)
    #plt.imshow(im1, interpolation='none', origin = 'lower', aspect = 165/binNum , cmap=plt.cm.gnuplot)
#    plt.imshow(im1, interpolation='none', origin = 'lower', aspect = aspect , cmap=plt.cm.gnuplot)
    #im1 = im1[1:]
    #plt.imshow(im1, interpolation='none', origin = 'lower' , cmap=plt.cm.gnuplot)
    #plt.axis('scaled')
    #plt.subplot(212)
    #plt.imshow(np.random.random((100, 100)), cmap=plt.cm.BuPu_r)
    
    pIllusStep = 10
    lam_beta = np.array(data_1.prange)[::pIllusStep]
    ticks = np.arange(len(data_1.prange))[::pIllusStep]
    strticks = tuple ( [ str( '{:.1e}'.format(i) ) for i in lam_beta ] )
    
    strticks = [ remove_zero(a) for a in strticks ]
    
    #ticks = np.arange(min(prange), max(prange), step=0.01)
    labels = lam_beta
    
    #plt.xticks(ticks, lam_beta, rotation='vertical')
    #ax.set_xticks(ticks, strticks, rotation='vertical')
    #ax.set_xticks(ticks)
    #ax.set_xticklabels(lam_beta, rotation = 'vertical')
    
    #ax.set_xticklabels(lam_beta)
    yticks = np.linspace(0, binNum , 11)[:-1]
    yticks = yticks - omitted_bins
    ytickvals = np.round (np.arange(0,1, 0.1, ) , 1) [yticks > 0]
    yticks = yticks [ yticks > 0 ]
    #omitted_ticks = np.sum(yticks>binNum)
    
    #ytickvals = ytickvals[ yticks < binNum ]
    #yticks = yticks[ yticks<binNum ]
    
    #ax.set_yticks(yticks, ytickvals)
    ax.set_xlabel('$p$')
    ax.set_ylabel('$ \\rho_{ab} $ \t')
    #plt.ticklabel_format(style='plain')
    #plt.ticklabel_format(style='sci', axis = 'x')
    
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.yaxis.major.formatter._useMathText = True

    ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    ax.xaxis.major.formatter._useMathText = True

    
    #plt.ylim([])

    #fig.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    #cax = plt.axes([0.80, 0.1, 0.035, 0.8])
    cbar = fig.colorbar(cs)
    
    cbar.ax.text(0 , im1.max()*1.02 , "$\\times 10 ^{{{}}} $".format( exponent ) ) 
    
    #cbar.set_ticklabels([r'$<10^{0}$', 1, 2, r'$10^{14}$', r'$10^{14}+12345678$'])
    #cbar.set_label('$\Pi( \\rho_{ab} )$', labelpad=+20, y=0.5)
    #cbar.set_label('$\Pi( \\rho_{ab} )$')
    cbar.ax.text(im1.max() * 4.5, im1.max() / 2, '$\Pi( \\rho_{ab} )$', rotation = 90)

    
    #https://stackoverflow.com/questions/25983218/scientific-notation-colorbar-in-matplotlib

    #name_string = "$normal$, " + dis_type + ", " + data_type + ", $n=$" + str(nrange[nindex]) + ", $p=$" + str(prange[pindex]) + ", $q=$" + str(qrange[qindex]) + ", $r=$" + str(rrange[rindex])
    #name_string = '$q=p$' + ", $n=$" + str(n) 
    #name_string = '$q=1$' + ", $n=$" + str(n)
    qtext = data_1.qrange[qindex]
    if ( 'non-coop' in str(data_1.f) ):
        qtext = 'p'

    name_string = '$q={}$'.format(qtext) + ', ' + '$r={}$'.format(data_1.rrange[data_1.rindex]) + ',' + data_1.data_type.replace('$',' ') # + ", $n=$" + str(n)
    #name_string = '$q=p$' + data_type.replace('$',' ') + ", $n=$" + str(n)
    #fig.suptitle(name_string)
    
    name_string = name_string.replace('$','')
    name_string = name_string.replace(' ','')
    name_string = name_string.replace('_','')
    name_string = name_string.replace('.','')
    #plt.savefig('/media/sepante/04762A4D762A4032/University/Network Project/Simulation/C++/Temporal SIR/Results/coin-R.png', dpi = 1000) # change the resolution of the saved image
    location = data_1.location

    
        
    fig.savefig(location+"histogram,"+ "ab," +name_string+".png", dpi = 300, bbox_inches='tight')
    #fig.savefig(location+"histogram, "+ "ab, " +name_string+".png", bbox_inches='tight')
    plt.show()

    #"""
##Kullback–Leibler divergence
#for i in range(1,len(hist)):
    #print( stats.entropy(hist[0]+0.00001, hist[i]+0.001) )