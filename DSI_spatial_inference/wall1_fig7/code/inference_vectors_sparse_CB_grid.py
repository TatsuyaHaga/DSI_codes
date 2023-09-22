#!/usr/bin/env python3

import numpy
import scipy.linalg
import sys

context = sys.argv[1]
rep=numpy.loadtxt(sys.argv[2], delimiter=",")
Ns = int(rep.shape[0]/3)
#if rep.shape[0] != 2*Ns:
#    print(f"Number of states did not match {rep.shape[0]}!={3*Ns}")
#    exit()

Nelem = int(sys.argv[4])

gridness = numpy.loadtxt(sys.argv[5], delimiter=",")
isgrid = gridness>0
isnongrid = numpy.logical_not(isgrid)

rep_A = rep[:Ns,:]
rep_B = rep[Ns:2*Ns,:]
rep_C = rep[2*Ns:3*Ns,:]

diff = numpy.sum((rep_B - rep_C)**2, axis=0)
diff[isnongrid] = -1
idx_sort = numpy.argsort(diff)
idx_max = idx_sort[-Nelem:]
idx_min = idx_sort[:Nelem]
print("maximum difference units:", idx_max)
print("minimum difference units (meaningless):", idx_min)

rep_AB = rep_A + 0.0
rep_AB[:,idx_max] = rep_A[:,idx_max] + rep_B[:,idx_max] - rep_C[:,idx_max]

rep_CB = rep_C + 0.0
rep_CB[:,idx_max] = rep_B[:,idx_max]

if context=="AB":
    rep_out = rep_AB
if context=="CB":
    rep_out = rep_CB
numpy.savetxt(sys.argv[3], rep_out, delimiter=",")
