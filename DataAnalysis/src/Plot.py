'''
Created on Dec 12, 2016

@author: Dima
'''
import csv
import numpy as np
from numpy import inf
import collections
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#filename = 'F:/GridSimResults/clustComp/3nodesResult.txt'
#filename = 'F:/GridSimResults/clustComp/BandwidthResult.txt'
filename = 'F:/GridSimResults/clustComp/cpuResults.txt'

appDict = collections.OrderedDict()
appDict['PLANNER'] = 0
appDict['PUSHseq'] = 1
appDict['PUSHpar'] = 2   

nAlgs = appDict.__len__()
nPoints = 16
nDatasets = 5

data = np.zeros( (nAlgs, nPoints, nDatasets), dtype=np.float64 )
pointDict = collections.OrderedDict()



appInd = 100500
pointInd = 100500
pointIterator = 0
with open(filename, newline='') as f:
    reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(row)
        appInd = appDict.get(row[0])
        if row[1] in pointDict.keys():
            pointInd = pointDict.get(row[1])
        else:
            pointInd = pointIterator            
            pointDict[row[1]] = pointInd
            pointIterator += 1
        data[appInd, pointInd, int(row[2]) - 1] = row[3]
        print(appInd)
        
        
        
#print('points: ')
#for point in pointDict.keys():
#    print(point)    

#data[data == 0] = 1
    
print(data)    

# Calculate improvement
improvement = np.zeros( (nAlgs - 1, nPoints, nDatasets), dtype=np.float64 )
for i in range(1, nAlgs) :
    improvement[i-1, :, :] = 100 * (data[i, :, :] - data[0, :, :]) / data[i, :, :]

print(improvement)

#calculate averages and deviation
averages = np.average(improvement,axis=2)
deviations = np.std(improvement,axis=2)
print(averages)
print(deviations)

# remove infinity
averages[averages == -inf] = 0 
deviations[deviations == -inf] = 0 

# prepare data for plotting
i = 0
x = np.zeros( nPoints);
for key in pointDict.keys():
    x[i] = key
    i += 1

# plot
colors = ['k', 'r', 'b']
patches = []
plt.figure()    
i = 0;
plannerName = ''
for key in appDict.keys():    
    if i == 0:
        plannerName = key
        i += 1
        continue
    points = np.zeros( (nPoints, 3));
    points[:,0] = x[:]
    points[:,1] = averages[i-1, :]
    points[:,2] = deviations[i-1, :]
    # to plot in x order
    points.view('float64,float64,float64').sort(order=['f0'], axis=0)
    print(key)
    print(points)
    line = plt.errorbar(points[:,0], points[:,1], yerr=points[:,2])
    lbl = plannerName + ' vs ' + key
    #set stile
    plt.setp(line, linewidth=1, color=colors[i], label=lbl)
    #for legend
    patch = mpatches.Patch(color=colors[i], label=lbl)
    patches.append(patch)
    i += 1
       
'''    
line1 = plt.errorbar(x[:], averages[0, :], yerr=deviations[0, :])

fit = np.polyfit(x[:], averages[0, :], 1)
fit_fn = np.poly1d(fit) 
#plt.plot(x[:], fit_fn(x), 'r-')

line2 = plt.errorbar(x[:], averages[1, :], yerr=deviations[1, :])
plt.setp(line2, zorder=1, color='b', linewidth=1, label="PLANNER vs PUSH_par")
fit2 = np.polyfit(x[:], averages[1, :], 5)
fit_fn2 = np.poly1d(fit2) 
#plt.plot(x[:], fit_fn2(x), 'b-')

patch1 = mpatches.Patch(color='red', label='PLANNER vs PUSH_seq')
patch2 = mpatches.Patch(color='blue', label='PLANNER vs PUSH_par')
'''
plt.legend(handles=patches, loc=2)


plt.xlabel('Number of CPUs')
plt.ylabel('Makespan improvement (%)')
plt.axis([900, 6100, 0, 18])
plt.show()