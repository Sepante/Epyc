import numpy as np
import matplotlib.pyplot as plt


import matplotlib
import pandas as pd
import scipy as sp
from scipy import optimize
import matplotlib.ticker as mtick
from matplotlib.ticker import FormatStrFormatter

#"""
def Burst(i_t_times):
    return ( np.std(i_t_times) - np.mean(i_t_times) ) / (np.std(i_t_times) + np.mean(i_t_times) )
    #r = np.std(i_t_times) / np.mean(i_t_times)
    #return (np.sqrt(n+1) * r - np.sqrt(n-1)) / ( (np.sqrt(n+2) - 2)*r + np.sqrt(n-1) )
    #return np.std(i_t_times)

#pd_data = pd.read_csv('clean_input_matrix.txt', sep ='\t', header = None)
#pd_data = pd.read_csv('primaryschool.csv', sep =',', header = None)
#pd_data = pd.read_csv('burst_creator/burst_graph.txt', sep ='\t', header = None)

#pd_data = pd.read_csv('network data/normal/normal clean sociopattern_hospital.txt', sep ='\t', header = None)
#pd_data = pd.read_csv('network data/normal/normal clean brazil.txt', sep ='\t', header = None)
#pd_data = pd.read_csv('network data/normal/normal clean sociopattern_conference_contact.txt', sep ='\t', header = None)
#pd_data = pd.read_csv('network data/clean/clean FilmMessages.txt', sep ='\t', header = None)
#pd_data = pd.read_csv('network data/clean/clean FilmForum.txt', sep ='\t', header = None)
#pd_data = pd.read_csv('network data/clean/clean email.txt', sep ='\t', header = None)
#file = "DCW-sh clean sociopattern_conference_contact.txt"
#filedir = "network data/shuffled/DCW/"
#filedir = "network data/giant/"
#file = "giant clean brazil.txt"
#filedir = "network data/shuffled/SOU/"

filedir = "network data/clean/"
#file = "clean sociopattern_hospital.txt"
#file = "giant clean primaryschool.txt"
file = "clean sociopattern_conference_contact.txt"

fullfile = filedir + file


pd_data = pd.read_csv(fullfile , sep ='\t', header = None)
#pd_data = pd.read_csv('network data/normal/normal clean brazil.txt', sep ='\t', header = None)
#pd_data = pd.read_csv('network data/normal/normal clean FilmMessages.txt', sep ='\t', header = None)
#pd_data = pd.read_csv('network data/clean/clean sociopattern_hospital.txt', sep ='\t', header = None)
temp_graph = np.array(pd_data)


#plt.suptitle( file + "# $of$ $contacts$")

#temp_graph[:, 0]= np.round( temp_graph[:, 0] / 1000 )

binNum = int (temp_graph[:,0].max() / 3600 )
hist, bins = np.histogram(temp_graph[:, 0], binNum)
widths = np.diff(bins)
#hist = hist / len( temp_graph[:, 0] )
#hist = hist / widths[0]

#pIllusStep = 1
#lam_beta = np.array(data_1.prange)[::pIllusStep]
#ticks = np.arange(len(data_1.prange))[::pIllusStep]
#strticks = tuple ( [ str( '{:.1e}'.format(i) ) for i in lam_beta ] )

#strticks = [ remove_zero(a) for a in strticks ]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)


ax.bar(bins[:-1], hist, widths,  color = 'orange', linewidth=1,   ec='black')
#plt.plot(bins[:-1], hist, '--o')
#ax.yaxis.set_label_coords(-0.08, 0.5)
ax.set_xlabel( '$t(s)$' )
ax.set_ylabel( '$C$' )



ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
#ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))

ax.yaxis.major.formatter._useMathText = True


ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))

ax.xaxis.major.formatter._useMathText = True

ratio =  (hist.max() / bins.max())

ax.set_aspect(0.5/ratio)

matplotlib.rcParams.update({'font.size': 16})

file = file.replace('_', '')
file = file.replace('.txt', '')
file = file.replace(' ', '')
#data_type = data_type.replace('giant ', '')


fig.savefig("contactnum-"+file+ "-ab" +".png" ,dpi = 300, bbox_inches='tight')
#fig.savefig("contactnum-"+file+ "-ab" +".png", bbox_inches='tight')
plt.show()
#plt.plot( bins[:-1], hist, widths, 'o' )
"""
mean = np.full( binNum , hist.mean())
#print(mean[0] )
#plt.plot(bins[:-1], mean , 'r--')

#the collective burst
##

time_stamps = temp_graph[:,0]
i_t_times = np.diff(time_stamps) #interevent times
print( Burst(i_t_times) )

time_stamps= np.round( time_stamps / 10000, 2 )

#time_stamps = temp_graph[:,0]
i_t_times = np.diff(time_stamps) #interevent times
print( Burst(i_t_times) )


#check if all the first nodes are smaller (in label) than the other.
t = 0

edge_list = temp_graph[:,1:]
for edge in edge_list:
    if edge[0] < edge[1]:
        t+=1


unique_rows = np.unique(edge_list, axis=0)
"""
"""
ind_burst = []
occurence_num = []
dummy = 0

#for edge_samp in temp_graph:
for edge_samp in unique_rows:
#for edge_samp in [np.array([0,3])]:
    dummy+=1
    if dummy % 100 == 0:
        print(dummy)
    times = []
    #edge_samp = temp_graph[]
    for edge in temp_graph:
        if edge_samp[0] == edge[1]:
            if edge_samp[1] == edge[2]:
                times.append( edge[0] )
                #print(times)
    times = np.diff(np.array(times))
    if(len(times)>=2):
        b = Burst(times)
        #print( b )
        ind_burst.append(b)
        occurence_num.append(len(times))
    
    #print(times.mean())
#"""
"""
opacity_num = 1
#plt.hist( occurence_num ,100)
hist, bins = np.histogram(occurence_num, 100 )
widths = np.diff(bins)

plt.bar(bins[:-1], hist, widths, linewidth=1, alpha = opacity_num, log = True)
plt.title(  file )
plt.xlabel('$edge-occurene$ $hitogram$')
#plt.xlim([0, 10])
plt.savefig( "edge-occurencet-hist " + file + ".png" )
plt.show()


#plt.hist(np.sort(ind_burst)[0:-9:1], 100)
plt.hist(ind_burst, 100)
plt.title(  file )
plt.xlabel('$edge-burst$ $histogram$')
plt.savefig( "edge-burst-hist " + file + ".png" )
plt.show()
#"""
"""
#plt.xlim([150, 300])
plt.xlabel('$edge$ $occurence$ $number$')
plt.ylabel('$burst$')
plt.plot((occurence_num), ind_burst,'o',alpha = 0.1)
plt.title(  "burst-occurence " + file )
plt.xscale('log')
plt.ylim([-1, 1])
#plt.xlim([ 0,50 ])
plt.savefig( "burst-occurence " + file + ".png" )

#bursty train calulation (works good for FilmMessages and FilmForum files.)
#"""
"""
l = []

temp_graph[:, 0]= np.round( temp_graph[:, 0] / 10 )
s = 1
wagonSize = 100
diffs = np.diff (temp_graph [:, 0] )
for i in ( diffs > wagonSize):
    if (i):
        s += 1

    if (not i):
        #if(s>1):
            #print(s)
        l.append(s)
        s = 1

l = np.array ( l )
hist, bins = np.histogram ( l, max(l) - min(l) )
widths = np.diff(bins)

#plt.plot(bins[1:-1], hist[1:], 'o', alpha = 0.25)
excludedPoints = 10
x = bins[excludedPoints:-1]

y =  hist[excludedPoints:]

#ans = sp.optimize.curve_fit(lambda t,b: b*np.exp(t),  x,  y)
def func(x, a, b):
    return (a*np.exp(-b * x))

#popt, pcov = sp.optimize.curve_fit(func, x, y, bounds=(0, [20000000, 1000]))

popt, pcov = sp.optimize.curve_fit(func, x, y)
perr = np.sqrt(np.diag(pcov))
#plt.plot( pcov )

#lt.plot(x, func(x, *popt), 'r-',label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
plt.plot(x, y,'co', alpha = 0.3)
plt.plot(x, func(x, *popt),'b-')
plt.suptitle( file + "$bursty$ $train$ $distribution$" + " wagon size = " + str(wagonSize))
#plt.sav
print(popt)
plt.savefig("r train, "+file + " " + name_string+" "+str(wagonSize)+" .png")
#"""