import sys
import itertools
import numpy
import pylab
import networkx
import pickle

def plot_network(filename, G, pos, title=None):
    #pylab.figure(figsize=(4,3))
    nc=networkx.draw_networkx_nodes(G,pos,node_color="black", node_size=0)
    networkx.draw_networkx_edges(G,pos)
    if title!=None:
        pylab.title(title,fontsize=20)
    pylab.axis("off")
    pylab.savefig(filename)
    pylab.close()

maze = numpy.loadtxt(sys.argv[1], delimiter=",")
#wall = 1

#node position
Nx, Ny = maze.shape
pos = {}
N = 0
for x in range(Nx):
    for y in range(Ny):
        if maze[x,y]==1:
            pos[N]=[x,y]
            N=N+1

edge_list=[]
for j,k in itertools.combinations(range(N),2):
    xdif = numpy.abs(pos[j][0]-pos[k][0])
    ydif = numpy.abs(pos[j][1]-pos[k][1])
    if (xdif + ydif <= 1):
        edge_list.append((j,k))

print(N, "nodes", len(edge_list), "edges")

G=networkx.Graph()
G.add_edges_from(edge_list)
plot_network("network_structure_wall.svg",G,pos)

graph_dump=(G,pos)
pickle.dump(graph_dump, open("graph_wall.pickle","wb"))