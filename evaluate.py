from scipy.special import comb, perm
from munkres import Munkres
import numpy as np

def getSet(fn):
    
    labelset = set();
    labelsmap = [];
    mset = set();
    n = 0;
    i = 0;
    with open(fn) as file:
        for line in file.readlines():
            line = line.split();
            id = line[0];
            #id = i;
            label = line[1];
#             if int(label) == 0:
#                 n = n + 1;
#             else:
            labelset.add(label)
            labelsmap.append([id,label])
            i += 1;
    valuemap = dict();
    for index,label in enumerate(labelset):
        valuemap[label] = index;
    num = len(labelset);
    print num
    sets = [set() for x in range(num)]
    i = num;
    for id,label in labelsmap:
#         if (int(label) == 0):
#             sets[i].add(id)
#             i = i + 1;
#         else:
        sets[valuemap[label]].add(id)
    
    return sets;

def loadSet(fn):
    
    labelset = set();
    labelsmap = [];
    mset = set();
    n = 0;
    i = 0;
    sets = [];
    ssets = set();
    msets = []
    with open(fn) as file:
        for line in file.readlines():
            line = line.split();
            a = set();
            sets.append(a)
            for k,j in enumerate(line):
                if k == 1:
                    continue
                sets[i].add(j)
                ssets.add(j)
                msets.append(j)
                n += 1;
            i += 1;  
            
    print len(ssets) 
    print 'num ',n
    
    return sets;

def precision(sets,grdsets):
    p = 0;
    num = 0;
    i = 0;j = 0;
    for set1 in sets:
        j = 0;
        for set2 in grdsets:
            tmpset = set1&set2;
            length = len(tmpset);
            if length > 1:
                length = comb(length, 2)
                num += length;
            j = j+1;
        i = i+1;
    all = 0;
    for set2 in sets:
        length = len(set2);
        if length > 1:
            length = comb(length, 2)
            all += length;
    p = (num+0.0)/all;
    

    return p;

def recall(sets,grdsets):
    r = 0;
    p = 0;
    num = 0;
    for set1 in sets:
        for set2 in grdsets:
            tmpset = set1&set2;
            length = len(tmpset);
            if length > 1:
                length = comb(length, 2)
                num += length;
    all = 0;
    for set2 in grdsets:
        length = len(set2);
        if length > 1:
            length = comb(length, 2)
            all += length;
    r = (num+0.0)/all;
    
    return r;

def f1(sets,grdsets):
    rc = recall(sets,grdsets);
    pr = precision(sets, grdsets)
    print "recall",rc,"precission",pr
    f = 2*pr*rc/(pr+rc);
    print "f1",f
    return f

def f2(sets,grdsets):
    rc = recall(sets,grdsets);
    pr = precision(sets, grdsets)
    print "recall",rc,"precission",pr
    f = 5*pr*rc/(4*pr+rc);
    print "f2",f
    return f

def best_map(L1,L2):
    #L1 should be the groundtruth labels and L2 should be the clustering labels we got
    Label1 = np.unique(L1)
    nClass1 = len(Label1)
    Label2 = np.unique(L2)
    nClass2 = len(Label2)
    nClass = np.maximum(nClass1,nClass2)
    G = np.zeros((nClass,nClass))
    for i in range(nClass1):
        ind_cla1 = L1 == Label1[i]
        ind_cla1 = ind_cla1.astype(float)
        for j in range(nClass2):
            ind_cla2 = L2 == Label2[j]
            ind_cla2 = ind_cla2.astype(float)
            G[i,j] = np.sum(ind_cla2 * ind_cla1)
    m = Munkres()
    index = m.compute(-G.T)
    index = np.array(index)
    c = index[:,1]
    newL2 = np.zeros(L2.shape)
    for i in range(nClass2):
        newL2[L2 == Label2[i]] = Label1[c[i]]
    return newL2   

def err_rate(gt_s, s):
    c_x = best_map(gt_s,s)
    err_x = np.sum(gt_s[:] != c_x[:])
    missrate = err_x.astype(float) / (gt_s.shape[0])
    return missrate 
