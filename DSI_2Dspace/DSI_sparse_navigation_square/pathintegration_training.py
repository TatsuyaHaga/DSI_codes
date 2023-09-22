#!/usr/bin/env python3

import numpy
import sys
from copy import copy
import pickle

W=numpy.loadtxt(sys.argv[1], delimiter=",")
rep = numpy.loadtxt(sys.argv[2], delimiter=",")
G,pos = pickle.load(open("graph.pickle", "rb"))

P,Ndim=rep.shape
if W.shape[0]!=P:
    print("state number invalid.")
    exit()

Nepisode = 100
Nstep_per_episode = 100000

#transition prob matrix
D=numpy.sum(W,axis=1)
prob = D/numpy.sum(D)
Dinv=D**-1
T=numpy.diag(Dinv)@W

#parameter
angle_dict = {(1,0):0, (1,1):1, (0,1):2, (-1,1):3, (-1,0):4, (-1,-1):5, (0,-1):6, (1,-1):7}
Nangle = len(angle_dict.keys())
A = numpy.random.rand(Nangle,Ndim,Ndim)
eta=0.01

#training
print("training start.")
#state_hist = []
for ep in range(Nepisode):
    state = numpy.random.randint(P) #start state
    error_mean = 0.0
    for t in range(Nstep_per_episode):
        #update hist
        #state_hist.append(state)
        #sample next state
        state_prev = state + 0
        state_onehot = numpy.random.multinomial(1, T[state,:])
        state = numpy.where(state_onehot==1)[0][0]
        move = (int(pos[state][0] - pos[state_prev][0]), int(pos[state][1] - pos[state_prev][1]))
        angle = angle_dict[move]
        error = rep[state] - A[angle,:,:]@rep[state_prev]
        A[angle] = A[angle] + eta*numpy.outer(error, rep[state_prev])
        error_mean += numpy.sum(error**2)

    #end of episode
    error_mean = error_mean / Nstep_per_episode
    #state_hist.append(-1)
    if (ep+1)%int(Nepisode//10)==0:
        print(ep+1, "/", Nepisode, "episodes", "error:", error_mean)

#save
numpy.save("direction_weight.npy", A)
#numpy.savetxt("state_seq.csv", state_hist, delimiter=",", fmt="%d")

