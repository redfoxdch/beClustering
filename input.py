#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

from numpy.core.numeric import inf
import numpy as np
from itertools import izip
import time

def calCosDistance(data):
    length = len(data)
    data = np.array(data)
    dim = len(data[0])
    dis = [[0 for i in range(length)] for line in range(length)]
        
    print "calculate distance\n"
    for i in range(length):
        for j in range(length):
            tmpdis = np.dot(data[i],data[j])
            dis[i][j] = tmpdis/np.sqrt(np.dot(data[i],data[i])*np.dot(data[j],data[j]))
    print "calculate distance end\n"
    
    distance = dis
    return distance

def calDistance(data):
    length = len(data)
    data = np.array(data)
    dim = len(data[0])
    dis = [[0 for i in range(length)] for line in range(length)]
        
    print "calculate distance\n"
    for i in range(length):
        for j in range(length):
	    tmpdata = data[i]-data[j]+0.0
            tmpdis = np.dot(tmpdata,tmpdata)
            dis[i][j] = np.sqrt(tmpdis)
            #print tmpdata,dis[i][j],tmpdata.shapes
    print "calculate distance end\n"
    
    distance = dis
    return distance

def getNeighbor(distance, thres):
    length = len(distance)
    rneighbor = [[] for nb in range(len(distance))]
    sum = 0;sum1 = 0;

    for i in range(length):
        dirc = dict()
        for j in range(length):
            dirc[j] = distance[i][j]
        sdirc = sorted(dirc.iteritems(), key = lambda d : d[1])
        for (k,dst) in sdirc: 
            if dst > thres:
                break
            if k != i:
                rneighbor[i].append(k)
                sum +=1
    neighbor = [[]for nb in range(length)];
    for i in range(length):
        dirc = dict()
        for j in range(length):
            dirc[j] = distance[i][j]
        sdirc = sorted(dirc.iteritems(), key = lambda d : d[1])
        j = 0;
        
        for (k,dst) in sdirc:
            if k==i:
                continue
            if len(neighbor[i]) >= 5 and dst > thres:  ## assign step can use different neighbor if there are some outliers should be put into larger clusters.
                pass
                break;
#             if dst > 2.2:
#                 break;
            neighbor[i].append(k)
            j += 1;
            sum1 +=1
    #for i,nb in enumerate(rneighbor):
    #    for j in nb: neighbor[j].append(i)
        
    print "sum",sum,sum1
    return neighbor,rneighbor


def loadDistance(fn):
    map = [];
    idsets = set()
    with open(fn) as file:
        while 1:
            line = file.readline()
            if line == '':
                break
            a,b,d = line.split();
            #a = int(a);b = int(b)
            #d = 1
            d = float(d);
            map.append([a,b,d])
            idsets.add(a)
            idsets.add(b)
    idmap = dict()
    i = 0;
    idsets = list(idsets)
    idsets.sort()
    for ids in idsets:
        idmap[ids] = i;
        i = i+1;
    length = len(idsets);
    dist = [[inf for jdist in range(length)] for idist in range(length)]
    for index in range(length):
        dist[index][index] = 0;
    for line in map:
        a,b,d = line[:];
        dist[idmap[a]][idmap[b]] = d;
    return dist,idmap

def loadNeighbor(fn, thres):
    max = 0
    t0 = time.time()
    with open(fn) as file:
        for line in file:
            #line = file.readline()
            if line == '':
                break
            a,b,d = line.split();
            a = int(a);b = int(b)
            #d = 1
            if a > max :
                max = a
            if b > max:
                max = b
    
    length = max + 1
    print length
    t1 = time.time()
    print t1 - t0
    rneighbor = [[] for nb in range(length)]
    neighbor = [[]for nb in range(length)];
    t2 = time.time()
    sum = 0;sum1 = 0;
    with open(fn) as file:
        for line in file:
            #line = file.readline()
            if line == '':
                break;
            a,b,d = line.split();
            a = int(a);b = int(b)
            d = float(d);
            if a == b:
                continue
            if d < thres :
                rneighbor[a].append(b);
                sum = sum+1;
            if d < thres or len(neighbor[a])< 5:## assign step can use different neighbor if there are some outliers should be put into larger clusters.
                neighbor[a].append(b)
                sum1 += 1
    t3 = time.time()
    print t1-t0,t2-t1,t3-t2;
    print "sum",sum,sum1

    return neighbor,rneighbor

def loadNeighbor(fn):
    max = 0
    t0 = time.time()
    i = 0;
    
    with open(fn) as file:
        
        for line in file:
            #line = file.readline()
            i = i + 1;
            if i == 1 :
                a,b = line.split()
                a = int(a);b = int(b)
                length = a;
                length = length + 1
                rneighbor = [[] for nb in range(length)]
                neighbor = [[]for nb in range(length)];
                continue;
            if line == '':
                break
            sp = line.split();
            a,b = [sp[0],sp[1]];
            a = int(a);b = int(b)
            if b > max:
                max = b
            for j in xrange(2,b+2):
                data = sp[j];
                data = int(data);
                neighbor[a].append(data);
                
    rneighbor = neighbor
    
    print length,i,max
    
    return neighbor,rneighbor


def saveDistance(fn,idmap,distance):
    ridmap = dict(izip(idmap.itervalues(),idmap.iterkeys()))
    i = 0;
    labelmap = []
    for idistance in distance:
        j = 0;
        for jdistance in idistance:
            labelmap.append([ridmap[i],ridmap[j],jdistance])
            j = j+1;
        i = i + 1;
    #labelmap = sorted(labelmap, key = lambda d:int(d[1]))
    #labelmap = sorted(labelmap, key = lambda d:int(d[0]))
    #print labelmap
    with open(fn,'w') as file:
        for idlabel in labelmap:
            if idlabel[0] != idlabel[1]:
                file.write(str(idlabel[0]));file.write(" ");file.write(str(idlabel[1]));file.write(" ");file.write(str(idlabel[2]));file.write("\n")
    return 

def saveLabels(fn,idmap,labels):
    ridmap = dict(izip(idmap.itervalues(),idmap.iterkeys()))
    i = 0;
    labelmap = []
    for label in labels:
        labelmap.append([ridmap[i],label])
        i = i + 1;
    #labelmap = sorted(labelmap, key = lambda d:int(d[0]))
    #print labelmap
    with open(fn,'w') as file:
        for idlabel in labelmap:
            file.write(str(idlabel[0]));file.write(" ");
            file.write(str(idlabel[1]));file.write("\n")
    
    return 

def saveLabel(fn,labels):
    i = 0;
    labelmap = []
    for label in labels:
        labelmap.append([i,label])
        i = i + 1;
    #labelmap = sorted(labelmap, key = lambda d:int(d[0]))
    #print labelmap
    with open(fn,'w') as file:
        for idlabel in labelmap:
            file.write(str(idlabel[0]));file.write(" ");
            file.write(str(idlabel[1]));file.write("\n")
    
    return 

def loadLabels(fn):
    labels = [];
    with open(fn) as file:
        for line in file.readlines():
            label = line.split();
            label = int(label[0])
            labels.append(label);
    return labels


