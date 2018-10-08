#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
"""
First version is very easy to understand the theory of boundary erosion clustering. all core codes less than 70 row.

LevelConstruction step takes O(n^2) time complexity, But fast version and labels assign takes O(nlogn) time complexity.

Note : In most case, neigbhor and rneighbor are the same, but you can define different neighbor and rneighbor for special need.
    for example, if you want to assign the outlier points to the main clusters, you may refer the k nearest neighbor witch is out range of radius r,
    thus neighbor may be more points than rneighbor.
"""
import Queue
def erosionCLustering(neighbor,rneighbor):
    level = levelConstructionFast(rneighbor)
    labels,centers = labelsAssign(level, neighbor)
    return labels,centers;
def levelConstruction(rneighbor): ##easy understood version
    length = len(rneighbor)   
    neighbor = [[] for nb in range(length)]
    for i,nb in enumerate(rneighbor):
        for j in nb: neighbor[j].append(i)
    level = [0 for x in range(length)]
    dense = [0 for x in range(length)]
    active = [1 for x in range(length)]
    for i in range(length):
            for j in rneighbor[i]:
                if active[j]:
                    dense[i] = dense[i] + 1
    mx = max(dense)
    iters = 1
    while 1:
        mindense = float('inf')#level  assign
        for i in range(len(rneighbor)):
            if active[i] & (mindense > dense[i]):
                mindense = dense[i]
        for j in range(len(dense)):
            if dense[j] == mindense and active[j]:
                active[j] = 0
                level[j] = iters
        if max(active) == 0:
            break;
        iters = iters + 1
        for i in range(len(dense)): #reconstruction dense
            dense[i] = 0  
        for i in range(len(rneighbor)):
            for j in rneighbor[i]:
                if active[j]:
                    dense[i] = dense[i] + 1
    return level

def labelsAssign(level, neighbor):
    length = len(level)
    labels = [0 for x in range(length)]
    idmap = [(i,level[i]) for i in range(length)]
    idmap = sorted(idmap, key = lambda d : d[1])
    idmap = [d[0] for d in idmap]
    centers = []
    idmap.reverse()
    num = 0
    labels = [0 for x in range(length)]
    num = 0
    for i in idmap:
        mlevel = level[i]
        for nid in neighbor[i]:
            if labels[nid] > 0:
                labels[i] = labels[nid]
		break
        if (labels[i] == 0):
            num = num + 1
            labels[i] = num
            centers.append(i)
    return labels,centers
    
"""
a fast version for Boundary Erosion clustering in level construciont step, construction step takes O(log(n)) time complexity
"""
class Node:
    def __init__(self, id, dense):
        self.id = id;
        self.dense = dense;
    def __lt__(self, other):
        return other.dense > self.dense
    def __str__(self):
        return "{}".format(self.dense)
     
def levelConstructionFast(rneighbor): ## nlog(n) version
    length = len(rneighbor)
    neighbor = [[] for nb in range(length)]
    for i,nb in enumerate(rneighbor):
        for j in nb: neighbor[j].append(i)   
    level = [0 for x in range(length)]
    dense = [0 for x in range(length)]
    active = [1 for x in range(length)]
    for i in range(length):
            for j in neighbor[i]:
                if active[j]:
                    dense[i] = dense[i] + 1
            dense[i] = dense[i];
    preq = Queue.PriorityQueue();
    for i in range(length):
        preq.put(Node(i,dense[i]))
    vset = set();
    nset = set();
    mind = min(dense);
    iters = 1
    while not preq.empty():
        #level assign for min density points 
        vset.clear()
        while not preq.empty():
            node = preq.get();
            d = node.dense;
            if mind >= d:
                mind = d;
                id = node.id;
                if active[id]:
                    vset.add(node.id)
            else:
                mind = d;
                preq.put(node)
                break;
        nset.clear()
        for id in vset:
            active[id] = 0
            level[id] = iters
            for j in rneighbor[id]:
                if active[j]:
                    nset.add(j);
        #recaculate density
        for id in nset:
            dense[id] = 0;
            for j in neighbor[id]:
                if active[j]:
                    dense[id] += 1;
            preq.put(Node(id,dense[id]))
        iters = iters + 1
    iters = iters - 1;
    return level
    
