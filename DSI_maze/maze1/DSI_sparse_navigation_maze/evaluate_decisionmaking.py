#!/usr/bin/env python3

import sys
import pickle
import numpy
import networkx
import pylab

adjacency = numpy.loadtxt(sys.argv[1], delimiter=",")
rep_from = numpy.loadtxt(sys.argv[2], delimiter=",")
rep_to = numpy.loadtxt(sys.argv[3], delimiter=",")

G,pos=pickle.load(open("graph.pickle","rb"))
G_wall,pos_wall=pickle.load(open("graph_wall.pickle","rb"))

Nstate, Drep = rep_from.shape
Nsim = 1000 #number of simulations
Nseq = 100 #maximum number of simulation steps
min_dist = 10 #minimum distance between start/goal 
familiarity_param = 1.0

def cos_sim(x, y):
    return numpy.sum(x*y,axis=1) / (numpy.linalg.norm(x,axis=1) * numpy.linalg.norm(y,axis=1))

def inner(x, y):
    return numpy.sum(x*y,axis=1)

shortest_path_results = []
count_steps_results = []
diff_pathlength = []
path_save = []
for trial in range(Nsim):
    #define start and goal
    idx_start = 0
    idx_goal = 0
    shortest_path_length = 0
    while shortest_path_length < min_dist:
        idx_start = numpy.random.randint(Nstate) #start
        idx_goal = numpy.random.randint(Nstate) #goal
        shortest_path_length = networkx.shortest_path_length(G, source=idx_start, target=idx_goal)
    pos_start = pos[idx_start]
    pos_goal = pos[idx_goal]
    vec_start = rep_from[idx_start,:]
    vec_goal = rep_to[idx_goal,:]

    #simulation
    vec_now = vec_start + 0.0 #current representation
    idx_now = idx_start + 0 #current state index
    pos_now = pos[idx_now] #current position
    vec_seq = [vec_now]
    idx_seq = [idx_now]
    pos_seq = [pos_now]
    count_steps = 0
    familiarity = numpy.zeros(Nstate)
    for i in range(Nseq):
        #candidates of next states
        idx_next = numpy.where(adjacency[idx_now,:]>0)[0] 

        #vector-based navigation
        value = inner(vec_goal.reshape((1,Drep)), rep_from[idx_next,:]) - familiarity[idx_next]
        idx_now = idx_next[numpy.argmax(value)]
        vec_now = rep_from[idx_now,:]
        pos_now = pos[idx_now]

        familiarity[idx_now] += familiarity_param

        vec_seq.append(vec_now)
        idx_seq.append(idx_now)
        pos_seq.append(pos_now)
        count_steps = count_steps + 1
        if idx_now == idx_goal:
            break

    shortest_path_results.append(shortest_path_length)
    count_steps_results.append(count_steps)
    diff_pathlength.append(count_steps-shortest_path_length)
    if len(path_save)<10:
        path_save.append((pos_start, pos_goal, pos_seq, count_steps-shortest_path_length))
    print(f"Trial {trial}: shortest path length={shortest_path_length}, simulation steps={count_steps}.")

optimal_ratio = numpy.sum(numpy.array(diff_pathlength)==0) #/ Nsim
path_length_ratio = numpy.array(count_steps_results)/numpy.array(shortest_path_results)
path_length_ratio_mean = numpy.mean(path_length_ratio)
success_rate = numpy.mean(path_length_ratio < 1.2)
print(f"Optimal navigation: {optimal_ratio} / {Nsim}")
print(f"Ratio of simulated path length to the shortest path length: {path_length_ratio_mean}")
print(f"Success rate (path length ratio < 1.2): {success_rate}")

#plot
def plt_setspines():
    pylab.gca().spines["right"].set_visible(False)
    pylab.gca().spines["top"].set_visible(False)
    pylab.gca().yaxis.set_ticks_position("left")
    pylab.gca().xaxis.set_ticks_position("bottom")

pylab.figure(figsize=(3,3))
plt_setspines()
pylab.hist(path_length_ratio, bins=10)#, log=True)
pylab.xlabel("Simulated path length \n/ shortest path length")
pylab.ylabel("#Trials")
pylab.tight_layout()
pylab.savefig("decision_making_hist.svg")
pylab.close()

max_dist = max(shortest_path_results)
pylab.figure(figsize=(3,3))
plt_setspines()
pylab.plot([min_dist-1, max_dist+1], [min_dist-1, max_dist+1], "--", color="gray") 
for i in range(Nsim):
    pylab.plot(shortest_path_results[i], count_steps_results[i], ".", color="black")
pylab.xlabel("Shortest path length")
pylab.ylabel("Simulation steps")
pylab.xlim([min_dist-1, max_dist+1])
pylab.ylim([min_dist-1, max(count_steps_results)+1])
pylab.tight_layout()
pylab.savefig("decision_making_steps.svg")
pylab.close()

for idx,path_recall in enumerate(path_save):
    pos_start, pos_goal, pos_seq, deviation = path_recall

    #nc=networkx.draw_networkx_nodes(G,pos,node_color="grey", node_size=5)
    #networkx.draw_networkx_edges(G,pos,edge_color="grey")
    nc=networkx.draw_networkx_edges(G_wall,pos_wall,edge_color="black")
    pylab.plot(pos_start[0] , pos_start[1], "o", label="Start")
    pylab.plot(pos_goal[0] , pos_goal[1], "o", label="Goal")
    pos_prev=pos_seq[0]
    for pos_now in pos_seq[1:]:
        #pylab.plot(pos_now[0], pos_now[1], "x", color="black")
        pylab.annotate("", xy=pos_now, xytext=pos_prev, arrowprops=dict(arrowstyle="-|>",facecolor="black", edgecolor="black"))
        pos_prev=pos_now
    pylab.legend()
    pylab.savefig("decision_making"+str(idx)+"_deviation"+str(deviation)+".svg")
    pylab.close()
