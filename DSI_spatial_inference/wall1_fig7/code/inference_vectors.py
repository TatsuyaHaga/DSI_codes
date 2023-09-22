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

rep_A = rep[:Ns,:]
rep_B = rep[Ns:2*Ns,:]
rep_C = rep[2*Ns:3*Ns,:]
rep_AB = (rep_A + rep_B - rep_C)

if context=="A":
    rep_out = rep_A
elif context=="B":
    rep_out = rep_B
elif context=="C":
    rep_out = rep_C
elif context=="AB":
    rep_out = rep_AB
numpy.savetxt(sys.argv[3], rep_out, delimiter=",")
