#!/usr/bin/env python3

import pylab
import numpy
import itertools
import networkx
import pickle
import sys

def plot_network(filename, G, pos, title=None):
    #pylab.figure(figsize=(4,3))
    nc=networkx.draw_networkx_nodes(G,pos,node_color="black", node_size=30)
    networkx.draw_networkx_edges(G,pos)
    if title!=None:
        pylab.title(title,fontsize=20)
    pylab.axis("off")
    pylab.savefig(filename)
    pylab.close()

def shape(x,y):
    r=30
    return x<r and y<r

#node position
Nx=120
Ny=120
pos={}
N=0
for x in range(Nx):
    for y in range(Ny):
        if shape(x,y):
            pos[N]=[x,y]
            N=N+1

edge_list=[]
for j,k in itertools.combinations(range(N),2):
    xdif=numpy.abs(pos[j][0]-pos[k][0])
    ydif=numpy.abs(pos[j][1]-pos[k][1])
    if (xdif<=1 and ydif<=1):
        edge_list.append((j,k))

print(N, "nodes", len(edge_list), "edges")

#Adjacency matrix
W=numpy.zeros([N,N])
for x in edge_list:
    W[x[0],x[1]]=1.0
    W[x[1],x[0]]=1.0

numpy.savetxt("edgelist.csv", numpy.array(edge_list), delimiter=",", fmt="%d")
numpy.savetxt("adjacency.csv", W, delimiter=",")

G=networkx.Graph()
G.add_edges_from(edge_list)
plot_network("network_structure.svg",G,pos)

graph_dump=(G,pos)
pickle.dump(graph_dump, open("graph.pickle","wb"))

