#!/usr/bin/env python3

import numpy
import sys
from copy import copy
import pickle
import pylab
import networkx

W=numpy.loadtxt(sys.argv[1], delimiter=",")
rep = numpy.loadtxt(sys.argv[2], delimiter=",")
A = numpy.load(sys.argv[3])
G,pos = pickle.load(open("graph.pickle", "rb"))

P,Ndim=rep.shape
if W.shape[0]!=P:
    print("state number invalid.")
    exit()

#setting
angle_list = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
angle_seq = [0]*5 + [1]*5 + [4]*20 +[7]*10 + [6]*10

#answer
state = 465 #start state
pos_start = pos[state]
x,y = pos_start
pos_seq_answer = [pos_start]
for angle in angle_seq:
    x += angle_list[angle][0]
    y += angle_list[angle][1]
    pos_seq_answer.append((x,y))

#path integration test
print("test start.")
#state_hist = []
pos_seq = []
pos_seq.append(pos[state])
rep_now = rep[state]
for angle in angle_seq:
    #state_hist.append(state)
    rep_now = A[angle]@rep_now
    state = numpy.argmin(numpy.sum((rep-rep_now.reshape((1,Ndim)))**2,axis=1))
    pos_seq.append(pos[state])

#plot
nc=networkx.draw_networkx_nodes(G,pos,node_color="grey", node_size=5)
networkx.draw_networkx_edges(G,pos,edge_color="grey")
pylab.plot(pos_start[0] , pos_start[1], "o", label="Start")
#pylab.plot(pos_goal[0] , pos_goal[1], "o", label="Goal")
pos_prev=pos_seq[0]
for pos_now in pos_seq[1:]:
    pylab.annotate("", xy=pos_now, xytext=pos_prev, arrowprops=dict(arrowstyle="-|>",facecolor="black", edgecolor="black"))
    pos_prev=pos_now
pylab.legend()
pylab.savefig("path_integration_test.svg")
pylab.close()

nc=networkx.draw_networkx_nodes(G,pos,node_color="grey", node_size=5)
networkx.draw_networkx_edges(G,pos,edge_color="grey")
pylab.plot(pos_start[0] , pos_start[1], "o", label="Start")
#pylab.plot(pos_goal[0] , pos_goal[1], "o", label="Goal")
pos_prev=pos_seq_answer[0]
for pos_now in pos_seq_answer[1:]:
    pylab.annotate("", xy=pos_now, xytext=pos_prev, arrowprops=dict(arrowstyle="-|>",facecolor="black", edgecolor="black"))
    pos_prev=pos_now
pylab.legend()
pylab.savefig("path_integration_answer.svg")
pylab.close()
