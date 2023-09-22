#!/usr/bin/env python3

import sys
import numpy
import scipy.linalg

#read data
W = numpy.loadtxt(sys.argv[1], delimiter=",")
vec_size = int(sys.argv[2])

#SVD
u,s,v = numpy.linalg.svd(W)
s_sqrt = numpy.diag(numpy.sqrt(s))
vec_left = u@s_sqrt
vec_right = (s_sqrt@v).T

#compress
vec_left = vec_left[:,:vec_size]
vec_right = vec_right[:,:vec_size]

#save
numpy.savetxt("vector_left.csv", vec_left, delimiter=",")
numpy.savetxt("vector_right.csv", vec_right, delimiter=",")
