# -*- coding: UTF-8 -*-
""" clustering via boundary erosion


    data   : 2018-1-30
    author : chenghao deng

"""
import Queue

def levelConstruction(neighbor):
    length = len(neighbor)
    rneighbor = [[] for x in range(length)]
    density = [0 for x in range(length)]
    for i,li in enumerate(neighbor):
        for id in li:
            rneighbor[id].append(i)
            density[i] += 1
    levels = [0 for x in range(length)]
    level = 0
    q = Queue.PriorityQueue()
    for i,d in enumerate(density):
        q.put((d,i))
    active = [1 for x in range(length)]
    mind = 0 
    while(not q.empty()):
        l = []
        d,id = q.get()
        mind = d
        if active[id]:
            l.append(id)
            active[id] = 0
        while(mind >= d and  not q.empty()):
            d,id = q.get()
            if active[id]:
                l.append(id)
                active[id] = 0;
        if mind < d :
            q.put((d,id))
        changeL = set()
        for id in l:
            levels[id] = level
            for nid in rneighbor[id]:
                if active[nid]:
                    density[nid] -= 1
                    changeL.add(nid)
        for id in changeL:
            q.put((density[id], id))
        level += 1  
    return levels

def labelAssign(neighbor,levels):
    length = len(neighbor)
    labels = [0 for x in range(length)]
    centers = []
    levelPair = [[-level, id] for id,level in enumerate(levels)]
    levelPair = sorted(levelPair, key = lambda d:d[0])
    label = 0
    for level,id in levelPair:
        for i in neighbor[id]:
            if labels[i] > 0:
                labels[id] = labels[i]
                break
        if labels[id] == 0:
            label += 1
            labels[id] = label
            centers.append(id)        
    return labels, centers

def labelAssignOutliers(neighbor,levels, topNeighbor, outliers = 3):    
    length = len(neighbor)
    labels = [0 for x in range(length)]
    centers = []
    levelPair = [[-level, id] for id,level in enumerate(levels)]
    levelPair = sorted(levelPair, key = lambda d:d[0])
    label = 0
    density = [0 for x in range(length)]
    for i,li in enumerate(neighbor):
        for id in li:
            density[i] += 1
    for level,id in levelPair:
        for i in neighbor[id]:
            if labels[i] > 0:
                labels[id] = labels[i]
                break
        if labels[id] == 0 and density[id] > outliers:
            label += 1
            labels[id] = label
            centers.append(id)
    for level,id in levelPair:
        for i in topNeighbor[id]:
            if labels[i] > 0:
                labels[id] = labels[i]
                break       
    return labels, centers

def beClustering(neighbor, topNeighbor = [], outliers = 3):
    print 'level construction\n'
    levels = levelConstruction(neighbor)
    print 'labels assign\n'
    if outliers == 0:
        labels, centers = labelAssign(neighbor,levels)
    else :
        labels,centers = labelAssignOutliers(neighbor, levels, topNeighbor, outliers)
    print 'clustering end\n'
    return labels, centers
