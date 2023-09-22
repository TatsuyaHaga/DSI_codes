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
Nx=20
Ny=20
pos={}
N=0
for x in range(Nx):
    for y in range(Ny):
        pos[N]=[x,y]
        N=N+1

def flag_wall(pos1, pos2, wall_pos, wall_max, wall_min, ax):
    flag1 = ((pos1[1-ax]==wall_pos-1 and pos2[1-ax]==wall_pos) or (pos1[1-ax]==wall_pos and pos2[1-ax]==wall_pos-1))
    flag2 = ((pos1[ax]>=wall_min and pos1[ax]<wall_max) or (pos2[ax]>=wall_min and pos2[ax]<wall_max))
    return (flag1 and flag2)

edge_list=[]
edge_list_A=[]
edge_list_B=[]
edge_list_AB=[]
for j,k in itertools.combinations(range(N),2):
    xdif=numpy.abs(pos[j][0]-pos[k][0])
    ydif=numpy.abs(pos[j][1]-pos[k][1])
    if (xdif<=1 and ydif<=1):
        edge_list.append((j,k))
        edge_list_A.append((j,k))
        edge_list_B.append((j,k))
        edge_list_AB.append((j,k))
        #remove connections at barrier
        if flag_wall(pos[j], pos[k], 8, 15, 5, 1): #wall1-1
            edge_list_A.pop()
            edge_list_AB.pop()
        elif flag_wall(pos[j], pos[k], 5,8,5,0): #wall1-2
            edge_list_A.pop()
            edge_list_AB.pop()
        elif flag_wall(pos[j], pos[k], 15,8,5,0): #wall1-2
            edge_list_A.pop()
            edge_list_AB.pop()
        elif flag_wall(pos[j], pos[k], 12, 15, 5, 1): #wall2-1
            edge_list_B.pop()
            edge_list_AB.pop()
        elif flag_wall(pos[j], pos[k], 5,15,12,0): #door2-2
            edge_list_B.pop()
            edge_list_AB.pop()
        elif flag_wall(pos[j], pos[k], 15,15,12,0): #door2-2
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
