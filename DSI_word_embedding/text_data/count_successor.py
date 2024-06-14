#!/usr/bin/env python3

import sys
import numpy
import multiprocessing

def count_func(pid, q, Nstate, state_begin, state_end, state_seq, gamma):
    Nstate_count = state_end - state_begin
    W = numpy.zeros([Nstate,Nstate_count])
    E = numpy.zeros(Nstate_count, dtype=int)
    trace = numpy.zeros(Nstate_count)
    traceON = numpy.zeros(Nstate_count, dtype=bool)
    #sample next state
    for state in state_seq:
        if state>=0:
            #exponential trace
            trace[traceON] = gamma * trace[traceON]
            #counts
            if state>=state_begin and state<state_end:
                idx = state - state_begin
                trace[idx] += 1.0
                traceON[idx] = True
                E[idx] += 1
            W[state][traceON] += trace[traceON]
        else:
            #End Of Document-> reset trace
            trace[:] = 0.0
            traceON[:] = False
    #return results
    for idx in range(Nstate_count):
        q.put((pid, state_begin+idx, E[idx], W[:,idx]))
    print(f"process {pid} end.")

#settings
state_seq = numpy.loadtxt(sys.argv[1], delimiter=",", dtype="int")
gamma = float(sys.argv[2])

maxprocess = 16

Nstep = len(state_seq)
Nstate = numpy.max(state_seq)+1
Nepisode = numpy.sum(state_seq<0)
Nstate_per_process = int(numpy.ceil(Nstate / maxprocess))
print(f"data length={Nstep-Nepisode}, Nepisode={Nepisode}, Nstate={Nstate}, gamma={gamma}")

#count
Nprocess = 0
process_arr = []
queue = multiprocessing.Queue()
for state_begin in range(0, Nstate, Nstate_per_process):
    state_end = state_begin + Nstate_per_process
    if state_end > Nstate:
        state_end = Nstate
    Nprocess += 1
    process_arr.append(multiprocessing.Process(target=count_func, args=(Nprocess, queue, Nstate, state_begin, state_end, state_seq, gamma)))
    process_arr[-1].start()
    print(f"process {Nprocess} start: state {state_begin} - {state_end}")

#sum counts
W = numpy.zeros([Nstate,Nstate])
E = numpy.zeros(Nstate, dtype=int)
received = numpy.zeros(Nstate, dtype=bool)
while True:
    pid, idx, Epart, Wpart = queue.get()
    E[idx] = Epart
    W[:,idx] = Wpart
    received[idx] = True
    if numpy.all(received):
        if not queue.empty():
            print("Something remains in queue.")
        break

#successor (row:from, col:to)
S = W.T/E.reshape((Nstate,1))

#save
numpy.savetxt("state_count.csv", E, delimiter=",", fmt="%d")
numpy.save("successor_count.npy", S)
print("end.")
