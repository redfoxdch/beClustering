#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

from sklearn.cluster import k_means
from sklearn.manifold import spectral_embedding
import numpy as np
import input
import scipy.io as sio
import bec
import matplotlib.pyplot as plt
import input
from input import loadDistance, saveLabels, loadLabels, saveDistance, saveLabel
from sklearn import cluster
from evaluate import err_rate


matfile = "/home/chenghaod/Deep-subspace-clustering-networks-master/spdataorl.mat";
datafile = "/home/chenghaod/be/bedemo/Deep-subspace-clustering-networks-master/Data/col20.mat"
name = datafile.split(".")
labelfile = name[0]+".label"
print labelfile
aj = sio.loadmat(datafile)
#print aj
mt = aj['fea']
#mt.dtype = 'int64'
grd = aj['gnd'][:,0]
#mat = sio.loadmat(matfile)
#mt = mat['kerNS']

#maps = spectral_embedding(affinity,n_components=40,eigen_solver='arpack')
# 
mt = np.array(mt);
#print mt[1][3:13],mt[2][4:12]
#print mt.shape
 
distances = input.calDistance(mt);  
#
sio.savemat('odis.mat',{'dis':distances})
 
distances = sio.loadmat('odis.mat')['dis']

#print affinity[0][1:30]
print distances[1][0:80]
print distances[2][0:80]
print distances[40][0:80]
# print distances[124][1664:1728]
# print distances[131][1664:1728]
# print distances[159][1664:1728]



#exit()

labels,centers = bec.beclustering(distances, 3500,70, 80)
print  'l',len(labels)
# _, labels, _ = k_means(mt, 40)
# labels += 1

# spectral = cluster.SpectralClustering(n_clusters=38, eigen_solver='arpack', affinity='precomputed',assign_labels='discretize')
# spectral.fit(affinity) 
# labels = spectral.fit_predict(affinity) + 1
sio.savemat('cluster.mat',{'labels':labels,'centers':centers})

saveLabel(labelfile,labels)

#sio.savemat('/home/chenghaod/SSC_ADMM_v1.1/labels.mat',{'groups':labels})

m = 38;n = 64
bg = [0 for x in range(m*n)];
for i in range(m):
    for j in range(n):
        bg[i*n+j] = i+1
        
labels = np.array(labels)
bg = np.array(grd)
#bg[0] = 41

#print labels
print max(bg),max(labels),min(bg),min(labels)
        


times = {}
for i in labels:
    if i not in times:
        times[i] = 1;
    else:
        times[i] += 1;
ts = sorted(times.iteritems(), key = lambda d:d[1], reverse = True)
#print ts
if max(bg) < max(labels):
	tmp = bg;bg = labels; labels = tmp;
eat = err_rate(bg, labels)
#eat = err_rate(labels,bg)         

print 'erro rate ', eat
print "class num:",max(labels)

