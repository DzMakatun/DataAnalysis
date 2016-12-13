'''
Created on Dec 12, 2016

@author: Dima
'''
import csv
import numpy as np
import collections
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


filename = 'F:/GridSimResults/clustComp/3nodesResult.txt'
appDict = collections.OrderedDict()
appDict['PLANNER'] = 0
appDict['PUSHseq'] = 1
appDict['PUSHpar'] = 2   

nAlgs = appDict.__len__()
nPoints = 14
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
plt.figure()
i = 0
x = np.zeros( nPoints);
for key in pointDict.keys():
    x[i] = key
    i += 1
line1 = plt.errorbar(x[:], averages[0, :], yerr=deviations[0, :])
plt.setp(line1, color='r', linewidth=1, label="PLANNER vs PUSH_seq")

line2 = plt.errorbar(x[:], averages[1, :], yerr=deviations[1, :])
plt.setp(line2, color='b', linewidth=1, label="PLANNER vs PUSH_par")

patch1 = mpatches.Patch(color='red', label='PLANNER vs PUSH_seq')
patch2 = mpatches.Patch(color='blue', label='PLANNER vs PUSH_par')
plt.legend(handles=[patch1,patch2],loc=4)


plt.xlabel('Bandwidth (Gbps)')
plt.ylabel('Makespan improvement (%)')
plt.show()