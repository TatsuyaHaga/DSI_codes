#!/usr/bin/env python3

import pylab
import numpy
import itertools
import networkx
import pickle
import sys
import copy

def plot_network(filename, G, pos, title=None):
    #pylab.figure(figsize=(4,3))
    nc=networkx.draw_networkx_nodes(G,pos,node_color="black", node_size=30)
    networkx.draw_networkx_edges(G,pos)
    if title!=None:
        pylab.title(title,fontsize=20)
    pylab.axis("off")
    pylab.savefig(filename)
    pylab.close()

#node position
Nx=21
Ny=21
pos={}
N=0
for x in range(Nx):
    for y in range(Ny):
        pos[N]=[x,y]
        N=N+1

edge_list=[]
edge_list_A=[]
edge_list_B=[]
edge_list_AB=[]
for j,k in itertools.combinations(range(N),2):
    xdif=numpy.abs(pos[j][0]-pos[k][0])
    ydif=numpy.abs(pos[j][1]-pos[k][1])
    #if (xdif<=1 and ydif==0) or (xdif==0 and ydif<=1):
    if (xdif<=1 and ydif<=1):
        edge_list.append((j,k))
        edge_list_A.append((j,k))
        edge_list_B.append((j,k))
        edge_list_AB.append((j,k))
        #remove connections at barrier
        #if ((pos[j][0]==6 and pos[k][0]==7) or (pos[j][0]==7 and pos[k][0]==6)) and ((pos[j][1]<12 or pos[k][1]<12) or (pos[j][1]>=16 or pos[k][1]>=16)):
        if ((pos[j][0]==6 and pos[k][0]==7) or (pos[j][0]==7 and pos[k][0]==6)) and ((pos[j][1]<14 or pos[k][1]<14)):
            edge_list_A.pop()
            edge_list_AB.pop()
        #if ((pos[j][0]==13 and pos[k][0]==14) or (pos[j][0]==14 and pos[k][0]==13)) and ((pos[j][1]<4 or pos[k][1]<4) or (pos[j][1]>=8 or pos[k][1]>=8)):
        if ((pos[j][0]==13 and pos[k][0]==14) or (pos[j][0]==14 and pos[k][0]==13)) and ((pos[j][1]>=7 or pos[k][1]>=7)):
            edge_list_B.pop()
            edge_list_AB.pop()

#Adjacency matrix
def get_adjacency(edges):
    W=numpy.zeros([N,N])
    for x in edges:
        W[x[0],x[1]]=1.0
        W[x[1],x[0]]=1.0
    return W

#numpy.savetxt("edgelist.csv", numpy.array(edge_list), delimiter=",", fmt="%d")
numpy.savetxt("adjacency.csv", get_adjacency(edge_list), delimiter=",")
numpy.savetxt("adjacency_A.csv", get_adjacency(edge_list_A), delimiter=",")
numpy.savetxt("adjacency_B.csv", get_adjacency(edge_list_B), delimiter=",")
numpy.savetxt("adjacency_AB.csv", get_adjacency(edge_list_AB), delimiter=",")

G=networkx.Graph()
G.add_edges_from(edge_list)
plot_network("network_structure.svg",G,pos)
G_A=networkx.Graph()
G_A.add_edges_from(edge_list_A)
plot_network("network_structure_A.svg",G_A,pos)
G_B=networkx.Graph()
G_B.add_edges_from(edge_list_B)
plot_network("network_structure_B.svg",G_B,pos)
G_AB=networkx.Graph()
G_AB.add_edges_from(edge_list_AB)
plot_network("network_structure_AB.svg",G_AB,pos)

pickle.dump((G,pos), open("graph.pickle","wb"))
pickle.dump((G_A,pos), open("graphA.pickle","wb"))
pickle.dump((G_B,pos), open("graphB.pickle","wb"))
pickle.dump((G_AB,pos), open("graphAB.pickle","wb"))
