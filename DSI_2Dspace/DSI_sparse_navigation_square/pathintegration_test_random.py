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

#size of the environment
Nx = 30
Ny = 30

def available_space(x,y):
    return (x>0 and x<Nx-1 and y>0 and y<Ny-1)

#setting
angle_list = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
Nangle = len(angle_list)

seq_len = 10
Ntrial = 1000
Nsuccess = 0

for trial in range(Ntrial):
    #print("trial"+str(trial))

    #generating answer
    pos_start = [-1,-1]
    while not available_space(pos_start[0], pos_start[1]):
        state_start = numpy.random.randint(P) #start state
        pos_start = pos[state_start]

    x,y = pos_start
    pos_seq_answer = [pos_start]
    angle_seq = []
    for i in range(seq_len):
        x_move = -1000
        y_move = -1000
        while not available_space(x+x_move, y+y_move):
            angle = numpy.random.randint(Nangle)
            x_move = angle_list[angle][0]
            y_move = angle_list[angle][1]
        x += x_move
        y += y_move
        pos_seq_answer.append((x,y))
        angle_seq.append(angle)

    #path integration test
    #state_hist = []
    state = state_start + 0
    #pos_seq = []
    #pos_seq.append(pos[state])
    rep_now = rep[state]
    success = True
    for t in range(seq_len):
        angle = angle_seq[t]
        #state_hist.append(state)
        rep_now = A[angle]@rep_now
        state = numpy.argmin(numpy.sum((rep-rep_now.reshape((1,Ndim)))**2,axis=1))
        #pos_seq.append(pos[state])
        if pos[state][0]!=pos_seq_answer[t+1][0] or pos[state][1]!=pos_seq_answer[t+1][1]:
            success = False
            break

    if success:
        Nsuccess += 1
    
print("trial:", Ntrial, "success:", Nsuccess, "success rate:", Nsuccess/Ntrial)
exit()
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
