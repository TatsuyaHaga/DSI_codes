#!/usr/bin/env python3

import numpy
import sys

name = sys.argv[1]

W1=numpy.loadtxt("adjacency_A.csv", delimiter=",")
W2=numpy.loadtxt("adjacency_B.csv", delimiter=",")
W3=numpy.loadtxt("adjacency.csv", delimiter=",")
P=W1.shape[0]
Wlist = [W1, W2, W3]
Ncontext = 3

Nepisode = 200
Nstep_per_episode = 100000
Nstep_switch = 1000

#transition prob matrix
Tlist = []
for W in Wlist:
    D=numpy.sum(W,axis=1)
    prob = D/numpy.sum(D)
    Dinv=D**-1
    Tlist.append(numpy.diag(Dinv)@W)

#generate a state sequence
print("sampling start.")
state_hist = []
for ep in range(Nepisode):
    state = numpy.random.randint(P) #start state
    idx_context = numpy.random.randint(Ncontext)
    T = Tlist[idx_context]
    for t in range(Nstep_per_episode):
        #update hist
        state_hist.append(state + idx_context*P)
        if (t+1)%Nstep_switch==0:
            #switch_context
            idx_context = idx_context + numpy.random.randint(1,Ncontext)
            idx_context = int(idx_context % Ncontext)
            #idx_context = numpy.random.randint(Ncontext)
            T = Tlist[idx_context]
        else:
            #sample next state
            state_onehot = numpy.random.multinomial(1, T[state,:])
            state = numpy.where(state_onehot==1)[0][0]

    #end of episode
    state_hist.append(-1)
    if (ep+1)%int(Nepisode//10)==0:
        print(ep+1, "/", Nepisode, "episodes")

#save
numpy.savetxt("state_seq"+name+".csv", state_hist, delimiter=",", fmt="%d")
print("end.")
