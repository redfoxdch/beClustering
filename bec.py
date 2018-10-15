import numpy as np
import Queue


def labelAssignOutliers(levels, neighbor,topNeighbor, outliers = 3):	
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
		for i in topNeighbor[id]:
			if labels[i] > 0:# and levels[id] >= levels[i]-2:
				labels[id] = labels[i]
				break;
			if labels[i] > 0 :
				labels[id] = labels[i]

		if labels[id] == 0 and density[id] > outliers:
			label += 1
			labels[id] = label

			centers.append(id)

	#for i in neighbor[id]:
	#		if labels[i] >= 0:
	#			labels[i] = labels[id]
			
	for id in range(length):
		for i in topNeighbor[id]:
			if labels[id] == 0 and labels[i] > 0 :#and levels[i] > levels[id] :
				labels[id] = labels[i]
				break	   
	return labels, centers

def labelsAssign(level,rneighbor, neighbor,outlierDense):
	length = len(level)
	labels = [0 for x in range(length)]
	idmap = [(i,level[i]) for i in range(length)]
	idmap = sorted(idmap, key = lambda d : d[1])
	idmap.reverse()
	#print idmap
	idmap = [d[0] for d in idmap]

	centers = []
	
	levelPair = [[-levels, id] for id,levels in enumerate(level)]
	levelPair = sorted(levelPair, key = lambda d:d[0])
	idmap = [d[1] for d in levelPair]
	#print levelPair
	labels = [0 for x in range(length)]
	num = 0
	dense = [0 for x in range(length)]
	for i in range(length):
			for j in rneighbor[i]:
				dense[i] = dense[i] + 1
			dense[i] = dense[i];
	
	for i in idmap:
		mlevel = level[i];
		for nid in rneighbor[i]:
			label = labels[nid]
		if label != 0 :
			labels[i] = label
			break;
			
			

		if (labels[i] == 0) and dense[i]>outlierDense: #outliers
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
	 
def levelConstructionFast(rneighbor,neighbor): ## nlog(n) version
	length = len(rneighbor)
	#neighbor = [[] for nb in range(length)]
	#for i,nb in enumerate(rneighbor):
	#	for j in nb: neighbor[j].append(i)   
	level = [0 for x in range(length)]
	dense = [0 for x in range(length)]
	active = [1 for x in range(length)]
	for i in range(length):
		for j in rneighbor[i]:
			if active[j]:
				dense[i] = dense[i] + 1
		dense[i] = dense[i];
	print 'max dense',max(dense)
	dense = np.array(dense)
	#dense = dense/2
	dense = [int(x) for x in dense]
	preq = Queue.PriorityQueue();
	for i in range(length):
		preq.put(Node(i,dense[i]))
	vset = set();
	nset = set();
	md = min(dense);
	iters = 1
	while not preq.empty():
		#level assign for min density points 
		vset.clear()
		mind = md
		while not preq.empty():
			node = preq.get();
			d = node.dense;
			k = 1
			#print 'd',d
			if mind >= d-k:
				md = d;
				#if mind >= d:				
				#	mind = d;
				#else :
				#	mind = d-k;
				id = node.id;
				if active[id]:
					vset.add(node.id)
					#break;
			else:
				md = d;
				preq.put(node)
				break
			#print 'nbk'
		#print len(vset)
		if len(vset) == 0:
			continue;
		nset.clear()

		for id in vset:
			active[id] = 0
			level[id] = iters
			for j in rneighbor[id]:
				if active[j]:
					nset.add(j);
			#dense[j] = dense[j] - 1.01
		#recaculate density
		for id in nset:
			dense[id] = 0
			for j in rneighbor[id]:
				if active[j]:
					dense[id] +=  1.0/3
			if dense[id] < md:
				md = dense[id]
			preq.put(Node(id,dense[id]))
		iters = iters + 1
		#print iters

	
	return level


def levelConstruction(neighbor):
	length = len(neighbor)
	rneighbor = [[] for x in range(length)]
	density = [0 for x in range(length)]
	for i,li in enumerate(neighbor):
		for id in li:
			rneighbor[id].append(i)
			density[i] += 1
	print 'ds',density
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
					density[nid] -= 1.01
					changeL.add(nid)
		for id in changeL:
			q.put((density[id], id))
		level += 1  
	return levels

def getNeighbor(distance, thres,topk = 0):
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
			if len(neighbor[i]) >= topk and dst > thres:  ## assign step can use different neighbor if there are some outliers should be put into larger clusters.
				pass
				break;
#			 if dst > 2.2:
#				 break;
			neighbor[i].append(k)
			j += 1;
			sum1 +=1
	for i,nb in enumerate(rneighbor):
		for j in nb: neighbor[j].append(i)
		

	print "sum",sum,sum1
	return neighbor,rneighbor

def beclustering(affinity, thres=0,outlierDense = 0, topk = 3):
	"""
	Returns
	-------
	labels : array of integers, shape: n_samples
		The labels of the clusters.
	centers : array of intergers, shape: cluster_num
	
	"""

	neighbor,rneighbor = getNeighbor(affinity, thres, topk)
	level = levelConstructionFast(rneighbor,neighbor)
	#print level
	#level = levelConstruction(rneighbor)
	print 'be lv',level

	labels,centers = labelAssignOutliers(level,rneighbor, neighbor,outlierDense)

	return labels,centers

