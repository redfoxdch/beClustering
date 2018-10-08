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



def demo(filename, thres):
	datafile = filename
	
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
	 


	distances = input.calDistance(data) 
	distances = np.array(distances)  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
	print 'dis',distances.shape

	print "getneighbor"


	a = thres
	nb,rnb = input.getNeighbor(distances,a)

	labels,centers = bec.beclustering(distances,a,5, 5)

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
		ax.text(data[i][0],data[i][1],"%i %i"%(level[i],density[i]))
	plt.show()
	#labels,centers = beclustering.beClustering(rnb,nb)
	#labels,centers = bclustering.erosionCLustering(nb,rnb)

	print "class num:",max(labels)
	
	print max(grd),max(labels),min(grd),min(labels)
	grd = np.array(grd)
	labels = np.array(labels) 
	labels = labels 

	draw.plot2d(labels,data)
	plt.show()    
	print grd.shape       
	eat = err_rate( labels,grd)  
	print 'error rate ',eat

def demo2(filename, thres):
	datafile = filename
	
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
	 


	distances = input.calDistance(data) 
	distances = np.array(distances)  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
	print 'dis',distances.shape

	print "getneighbor"


	a = thres
	nb,rnb = input.getNeighbor(distances,a)

	labels,centers = bec.beclustering(distances,a,5, 5)

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
		ax.text(data[i][0],data[i][1],"%i %i"%(level[i],density[i]))
	plt.show()
	labels,centers = beclustering.beClustering(rnb,nb)
	#labels,centers = bclustering.erosionCLustering(nb,rnb)

	print "class num:",max(labels)
	
	print max(grd),max(labels),min(grd),min(labels)
	grd = np.array(grd)
	labels = np.array(labels) 
	labels = labels 

	draw.plot2d(labels,data)
	plt.show()    
	print grd.shape       
	eat = err_rate( labels,grd)  
	print 'error rate ',eat

if __name__ == '__main__':
	demo2('jain.txt',3.8)
	demo('Aggregation.txt',1.5)
	demo('flame.txt',1.5)
	demo('jain.txt',3.8)
	demo('pathbased.txt',2.5)
	demo('sparil.txt',1.4)
	demo('s3.txt',40000)
	

