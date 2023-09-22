#!/usr/bin/env python3

import sys
import numpy
import scipy.stats
import pylab

dirs = ["trial1", "trial2", "trial3", "trial4", "trial5"]
vecs = ["A", "B", "C", "AB"]
contexts = ["A", "B", "AB"]

data = numpy.zeros([len(dirs), len(vecs), len(contexts)])

for i in range(len(dirs)):
    for j in range(len(vecs)):
        for k in range(len(contexts)):
            dirname = dirs[i]+"/navigation_"+vecs[j]+"_"+contexts[k]+"/"
            fname = "decisionmaking_result.txt"
            print(dirname, fname)
            with open(dirname+fname) as f:
                text = f.readlines()[-2]
                data[i,j,k] = float(text.split()[-1])

data_repA = data[:,0,:] #Vector A in A, B, A+B
data_repB = data[:,1,:] #Vector B
data_repC = data[:,2,:] #Vector phi (C)
data_repAB = data[:,3,:] #Vector A+B-phi

#statistical analysis
stat_vals = []
p_vals = []
stat, p = scipy.stats.ttest_ind(data_repA[:,2], data_repAB[:,2]) #A vs A+B
stat_vals.append(stat)
p_vals.append(p)
stat, p = scipy.stats.ttest_ind(data_repB[:,2], data_repAB[:,2]) #B vs A+B
stat_vals.append(stat)
p_vals.append(p)
stat, p = scipy.stats.ttest_ind(data_repC[:,2], data_repAB[:,2]) #phi vs A+B
stat_vals.append(stat)
p_vals.append(p)

numpy.savetxt("stat_vals.csv", stat_vals, delimiter=",", fmt="%f")
numpy.savetxt("p_vals.csv", p_vals, delimiter=",", fmt="%f")

#plot
def plt_setspines():
    pylab.gca().spines["right"].set_visible(False)
    pylab.gca().spines["top"].set_visible(False)
    pylab.gca().yaxis.set_ticks_position("left")
    pylab.gca().xaxis.set_ticks_position("bottom")

pylab.figure(figsize=(3,3))
plt_setspines()
xpos = numpy.arange(3)+0.5
width = 0.2
pylab.bar(xpos-1.5*width, numpy.mean(data_repA, axis=0), width=width, label="Vector A")
for i in range(data_repA.shape[0]):
    pylab.errorbar(xpos-1.5*width+i*0.02-0.05, data_repA[i,:], fmt=".", color="black")
pylab.bar(xpos-0.5*width, numpy.mean(data_repB, axis=0), width=width, label="Vector B")
for i in range(data_repA.shape[0]):
    pylab.errorbar(xpos-0.5*width+i*0.02-0.05, data_repB[i,:], fmt=".", color="black")
pylab.bar(xpos+0.5*width, numpy.mean(data_repC, axis=0), width=width, label=r"Vector $\Phi$")
for i in range(data_repA.shape[0]):
    pylab.errorbar(xpos+0.5*width+i*0.02-0.05, data_repC[i,:], fmt=".", color="black")
pylab.bar(xpos+1.5*width, numpy.mean(data_repAB, axis=0), width=width, label=r"Vector A+B-$\Phi$")
for i in range(data_repA.shape[0]):
    pylab.errorbar(xpos+1.5*width+i*0.02-0.05, data_repAB[i,:], fmt=".", color="black")
pylab.ylim([1.0,6.5])
pylab.xticks(xpos, contexts)
pylab.xlabel("Spatial context")
pylab.ylabel("Average path length \n (relative to the shortest path)")
pylab.legend()
pylab.tight_layout()
pylab.savefig("summary_spatial_composition.svg")
pylab.close()


