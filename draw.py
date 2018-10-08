# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.mlab import griddata

def plot2d(labels, data):
    data = np.array(data)
    labels = np.array(labels+1)
    f2 = plt.figure(1) 
    p1 = plt.subplot(111)
    num = max(labels)+1
    
    colorss = cm.rainbow(np.linspace(0, 1, num+1))
    #colors.cnames.items()[label*4+2]
    for label in range(num):
        idx = []
        for j in range(len(labels)):
            if labels[j] == label:
                idx.append(j)
                cn = colors.cnames.items()[label*4+2]
        for id in idx:
            p1.scatter(data[id,0], data[id,1], c = colorss[label], s = 30) 

        if label == 0:
            for id in idx:
                p1.scatter(data[id,0], data[id,1], c = 'k', s = 30) 
             
    #plt.figtext(0.1,0.93,"B", fontsize = 20, color = 'k');
    
    #p1.scatter(data[centers,0],data[centers,1], c = 'k', s = 30)
    #plt.axis([0,10**6,0,10**6])
    #p1.set_xticks([])
    #p1.set_yticks([])
    #p1.spines['right'].set_color('none')
    #p1.spines['top'].set_color('none')
    #p1.spines['bottom'].set_color('none')
    #p1.spines['left'].set_color('none')
   
    print "end"
    plt.show()
    return 

def demo(level, neighbor, data):
    data = np.array(data)
    level = np.array(level)
    
    num = max(level)+1
    
    f3 = plt.figure(2)
    dense = [0 for i in range(len(data))]
    
    for i in range(len(data)):
        dense[i] = len(neighbor[i])
    dense = np.array(dense)
    colors = cm.rainbow(np.linspace(0, 1, max(dense)+1))
    print "maxdesnse",max(dense)
    for i in range(len(data)):
        p1 = plt.scatter(data[i,0], data[i,1], c = colors[dense[i]], s = 30)
    
    plt.figtext(0.1,0.93,"A", fontsize = 20, color = 'k');
    f2 = plt.figure(3)
    colors = cm.rainbow(np.linspace(0, 1, num))
    for label in range(num):
        idx = []
        for j in range(len(level)):
            if level[j] == label:
                idx.append(j)
                
        for id in idx:
            p1 = plt.scatter(data[id,0], data[id,1], c = colors[label], s = 30)  
    
    plt.figtext(0.1,0.93,"B", fontsize = 20, color = 'k');        
    plt.savefig("level.pdf",dpi = 200)       
    x = data[:,0];y = data[:,1];z = level;
    # define grid.
    #xi = np.linspace(0, 40, 800)
    #yi = np.linspace(0, 35, 800)
    # grid the data.
    #z = griddata(x, y, z, x, y, interp='linear')
    #dense = griddata(x, y, dense, x, y, interp='linear')
    #x,y = np.meshgrid(x,y)
    #print 'sp',xi.shape,yi.shape,z.shape,dense.shape
    
    f4 = plt.figure(4)
    ax = Axes3D(f4)
    ax.view_init(55, 55)
    #x = x.flatten();y = y.flatten();z = z.flatten();
    print 'zs',z.shape
    ax.plot_trisurf(x, y, z, cmap='rainbow')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Level')
    plt.figtext(0.1,0.93,"D", fontsize = 20, color = 'k');
    f5 = plt.figure(5)
    ax1 = Axes3D(f5)
    ax1.view_init(55, 55)
    ax1.plot_trisurf(x, y, dense, cmap = 'rainbow')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Density')
    plt.figtext(0.1,0.93,"C", fontsize = 20, color = 'k');
    print "end"
    
    return
