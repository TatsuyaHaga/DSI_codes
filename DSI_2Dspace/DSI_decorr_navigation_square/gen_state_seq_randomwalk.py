#!/usr/bin/env python3

import numpy
import sys
from copy import copy

W=numpy.loadtxt(sys.argv[1], delimiter=",")
P=W.shape[0]

Nepisode = 500
Nstep_per_episode = 100000

#transition prob matrix
D=numpy.sum(W,axis=1)
prob = D/numpy.sum(D)
Dinv=D**-1
T=numpy.diag(Dinv)@W

#generate a state sequence
print("sampling start.")
state_hist = []
for ep in range(Nepisode):
    state = numpy.random.randint(P) #start state
    for t in range(Nstep_per_episode):
        #update hist
        state_hist.append(state)
        #sample next state
        state_onehot = numpy.random.multinomial(1, T[state,:])
        state = numpy.where(state_onehot==1)[0][0]

    #end of episode
    state_hist.append(-1)
    if (ep+1)%int(Nepisode//10)==0:
        print(ep+1, "/", Nepisode, "episodes")

#save
numpy.savetxt("state_seq.csv", state_hist, delimiter=",", fmt="%d")

