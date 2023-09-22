#!/usr/bin/env python3

import numpy
import sys
import matplotlib.pyplot as plt
import scipy.stats

def plt_setspines():
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().yaxis.set_ticks_position("left")
    plt.gca().xaxis.set_ticks_position("bottom")

rep1=numpy.loadtxt(sys.argv[1], delimiter=",")
rep2=numpy.loadtxt(sys.argv[2], delimiter=",")
P,D=rep1.shape

gridness=numpy.loadtxt(sys.argv[3], delimiter=",")

#distance
dist = numpy.zeros(D)
for idx in range(D):
    dist[idx] = numpy.sqrt(numpy.sum((rep1[:,idx]-rep2[:,idx])**2))

finite = numpy.isfinite(gridness)
isgrid = (gridness>0)
notgrid = numpy.logical_not(isgrid)
dist_grid = dist[isgrid]
dist_nongrid = dist[notgrid]
numpy.savetxt("dist_grid.csv", dist_grid, delimiter=",")
numpy.savetxt("dist_nongrid.csv", dist_nongrid, delimiter=",")

plt.figure(figsize=(3,3))
plt.plot(numpy.arange(len(dist_grid))/len(dist_grid)-0.5, dist_grid, ".")
plt.plot(numpy.arange(len(dist_nongrid))/len(dist_nongrid)+1.0, dist_nongrid, ".")
plt.xticks([0,1.5], ["Grid", "Non-grid"])
plt.ylabel("Representational distance")
plt.tight_layout()
plt.savefig("analysis_contextchange_divide.svg")
plt.close()

