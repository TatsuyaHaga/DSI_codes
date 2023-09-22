#!/usr/bin/env python3

import numpy
import sys

#read data
state_seq = numpy.loadtxt(sys.argv[1], delimiter=",", dtype="int")
win_size = int(sys.argv[2])

Nstep = len(state_seq)
Nstate = numpy.max(state_seq)+1
print(f"data length={Nstep}, Nstate={Nstate}, win_size={win_size}")

#learning
W = numpy.zeros([Nstate,Nstate])
E = numpy.zeros(Nstate)
state_count = 0
state_buffer = []
Nepisode = 0
print("Learning start.")
for t in range(Nstep):
    #sample next state
    state = state_seq[t]
    if state>=0:
        #counts
        for state_prev in state_buffer:
            W[state,state_prev] += 1
            W[state_prev,state] += 1
        E[state] += 1
        state_count += 1
        #keep new state
        state_buffer.append(state)
        #remove the oldest state
        if len(state_buffer)>win_size:
            state_buffer.pop(0)
    else:
        state_buffer.clear() #state<0 = end of episode
        Nepisode += 1

    if (t+1)%(Nstep//10)==0:
        print(f"{int((t+1)/(Nstep//10))}/10 {t+1} steps, {Nepisode} episodes") 

#PPMI
PPMI = W * state_count / numpy.outer(E,E)
PPMI[PPMI<=1.0] = 1.0 #truncate non-negative elements (log)
PPMI = numpy.log(PPMI)
numpy.savetxt("PPMI.csv", PPMI, delimiter=",")

print("finished.")
