#!/usr/bin/env python3

import sys
sys.path.append("../")

import numpy
import pylab
import itertools
import networkx
import pickle

def plot_network(filename, G, pos, title=None):
    #pylab.figure(figsize=(4,3))
    nc=networkx.draw_networkx_nodes(G,pos,node_color="black", node_size=30)
    networkx.draw_networkx_edges(G,pos)
    if title!=None:
        pylab.title(title,fontsize=20)
    pylab.axis("off")
    pylab.savefig(filename)
    pylab.close()

L=20
N=L**2
group_id=numpy.zeros(N)
group=[[],[],[],[]]

#node position
pos={}
for i in range(N):
    pos[i]=[int(i%L), int(i//L)]

xcut=int(0.7*L)
ycut=int(0.3*L)
bridge1 = int(0.2*L)
bridge2 = int(0.9*L)
bridge3 = int(0.8*L)
bridge4 = int(0.1*L)

for x in range(0,xcut):
    for y in range(0,ycut):
        group[0].append(x+L*y)
        group_id[x+L*y]=0

for x in range(0,xcut):
    for y in range(ycut,L):
        group[1].append(x+L*y)
        group_id[x+L*y]=1

for x in range(xcut,L):
    for y in range(ycut,L):
        group[2].append(x+L*y)
        group_id[x+L*y]=2

for x in range(xcut,L):
    for y in range(0,ycut):
        group[3].append(x+L*y)
        group_id[x+L*y]=3

edge_list=[]
for i in range(len(group)):
    for j,k in itertools.combinations(group[i],2):
        xdif=numpy.abs(j%L-k%L)
        ydif=numpy.abs(j//L-k//L)
        if xdif<=1 and ydif<=1:
            edge_list.append([j,k])

for x1,y1,x2,y2 in [[bridge1,ycut-1,bridge1,ycut], [bridge2-1,ycut-1,bridge2-1,ycut]]:
    edge_list.append([x1+L*y1,x2+L*y2])
    edge_list.append([x1+1+L*y1,x2+L*y2])
    edge_list.append([x1+L*y1,x2+1+L*y2])
    edge_list.append([x1+1+L*y1,x2+1+L*y2])
    edge_list.append([x1-1+L*y1,x2+L*y2])
    edge_list.append([x1+L*y1,x2-1+L*y2])
    edge_list.append([x1-1+L*y1,x2-1+L*y2])

for x1,y1,x2,y2 in [[xcut-1,bridge3,xcut,bridge3], [xcut-1,bridge4,xcut,bridge4]]:
    edge_list.append([x1+L*y1,x2+L*y2])
    edge_list.append([x1+L*(y1+1),x2+L*y2])
    edge_list.append([x1+L*y1,x2+L*(y2+1)])
    edge_list.append([x1+L*(y1+1),x2+L*(y2+1)])
    edge_list.append([x1+L*(y1-1),x2+L*y2])
    edge_list.append([x1+L*y1,x2+L*(y2-1)])
    edge_list.append([x1+L*(y1-1),x2+L*(y2-1)])

map(tuple, edge_list)

#Adjacency matrix
W=numpy.zeros([N,N])
for x in edge_list:
    W[x[0],x[1]]=1.0
    W[x[1],x[0]]=1.0

numpy.savetxt("edgelist.csv", numpy.array(edge_list), delimiter=",", fmt="%d")
numpy.savetxt("group_id.csv", group_id, delimiter=",", fmt="%d")
numpy.savetxt("adjacency.csv", W, delimiter=",")

G=networkx.Graph()
G.add_edges_from(edge_list)
plot_network("network_structure.svg",G,pos)

graph_dump=(G,pos)
pickle.dump(graph_dump, open("graph.pickle","wb"))
