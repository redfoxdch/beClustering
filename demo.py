#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import numpy as np
import input
import scipy.io as sio
import bec
import draw
import bclustering
import beclustering
from sklearn import cluster
from evaluate import err_rate
import matplotlib.pyplot as plt
from input import loadDistance, saveLabels, loadLabels, saveDistance, saveLabel

datafile = "jain.txt";
#datafile = "collins2007.txt"
name = datafile.split(".")
distfile = name[0] + ".out"
labelfile = name[0]+".label"

row = 0;dim = 0;
 
with open(datafile) as fp:
    lines = fp.readline()
    dim = len(lines.split())
data = []
n = 0
grd = [];
with open(datafile) as fp:
    for line in fp:
        tmpdata = line.split()
        tmpdata = [float(x) for x in tmpdata]
        if len(tmpdata) == 0:
            break
        data.append([tmpdata[0],tmpdata[1]])
        grd.append(tmpdata[2])
        n = n+1
#    


distances = input.calDistance(data)   
distances = np.array(distances)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
print 'dis',distances.shape
# #distfile = "brown.txt"
# name = distfile.split(".")
#distances,idmap = loadDistance(distfile);
#saveDistance("data20.txt",idmap,distances)
#distances = [[x for x in idist] for idist in distances]
print "getneighbor"


a = 3.8
nb,rnb = input.getNeighbor(distances,a)

labels,centers = bec.beclustering(distances,a,5, 0)
#level = bec.levelConstruction(rnb)
level = bec.levelConstructionFast(rnb)
#draw.demo(level, rnb, data)
fig,ax=plt.subplots()
data = np.array(data)
print data.shape
ax.scatter(data[:,0],data[:,1],c='r')
length = len(rnb)
rneighbor = [[] for x in range(length)]
density = [0 for x in range(length)]

for i,li in enumerate(rnb):
    for id in li:
        density[i] += 1

for i in range(len(level)):
	#pass
	#print data[i][0],level[i]
	ax.text(data[i][0],data[i][1],"%i %i"%(level[i],density[i]))
plt.show()
#labels,centers = beclustering.beClustering(rnb,nb)
#labels,centers = bclustering.erosionCLustering(nb,rnb)
#saveLabels(labelfile,idmap,labels)
#saveLabel(labelfile,labels)


#spectral = cluster.SpectralClustering(n_clusters=15)#, eigen_solver='arpack', affinity='precomputed',assign_labels='kmeans')
#spectral.fit(data)
#labels = spectral.fit_predict(data) + 1
#_, labels, _ = cluster.k_means(data,15)

print "class num:",max(labels)
#labels = loadLabels('data2_clabels.txt')
#print max(labels),min(labels)
#import exev
print max(grd),max(labels),min(grd),min(labels)
grd = np.array(grd)
labels = np.array(labels) 
labels = labels 

draw.plot2d(labels,data)
#draw.demo(level, neighbor,data)
plt.show()    
print grd.shape       
eat = err_rate( labels,grd)  
print 'error rate ',eat

