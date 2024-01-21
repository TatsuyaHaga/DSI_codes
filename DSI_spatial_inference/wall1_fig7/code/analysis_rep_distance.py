#!/usr/bin/env python3

import numpy
import scipy.stats
import sys
import matplotlib.pyplot as plt

def plt_setspines():
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().yaxis.set_ticks_position("left")
    plt.gca().xaxis.set_ticks_position("bottom")

rep1=numpy.loadtxt(sys.argv[1], delimiter=",")
rep2=numpy.loadtxt(sys.argv[2], delimiter=",")
P,D=rep1.shape

isgrid = numpy.loadtxt(sys.argv[3], delimiter=",")>0
notgrid = numpy.logical_not(isgrid)

gridness = numpy.loadtxt(sys.argv[4], delimiter=",")
finite = numpy.isfinite(gridness)

#distance
dist = numpy.zeros(D)
for idx in range(D):
    dist[idx] = numpy.sqrt(numpy.sum((rep1[:,idx]-rep2[:,idx])**2))

dist_grid = dist[isgrid]
dist_nongrid = dist[notgrid]
numpy.savetxt("dist_grid.csv", dist_grid, delimiter=",")
numpy.savetxt("dist_nongrid.csv", dist_nongrid, delimiter=",")

plt.figure(figsize=(3,3))
plt.plot(numpy.arange(len(dist_grid))/len(dist_grid)-0.5, dist_grid, ".", color="black")
plt.plot(numpy.arange(len(dist_nongrid))/len(dist_nongrid)+1.0, dist_nongrid, ".", color="black")
plt.xticks([0,1.5], ["Grid", "Non-grid"])
plt.ylabel("Representational distance")
plt.tight_layout()
plt.savefig("analysis_grid_dist_divide.svg")
plt.close()

print(scipy.stats.pearsonr(gridness[finite], dist[finite]))
r, p = scipy.stats.pearsonr(gridness[finite], dist[finite])
plt.figure(figsize=(2.5,2.5))
plt.plot(gridness[finite], dist[finite], ".", markersize=3, color="black")
plt.ylabel("Representaional distance")
plt.xlabel("Gridness")
plt.text(0.0, numpy.max(dist[finite])*(3/4), f"r={r:.2f}\np={p:.1g}", fontsize=10)
plt.tight_layout()
plt.savefig("analysis_grid_dist_cor.svg")
plt.close()