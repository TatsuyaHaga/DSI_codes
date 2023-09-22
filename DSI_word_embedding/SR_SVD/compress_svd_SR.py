#!/usr/bin/env python3

import sys
import numpy
import scipy.linalg

#read data
W = numpy.load(sys.argv[1])
vec_size = int(sys.argv[2])

W = W.T

#SVD
u,s,v = numpy.linalg.svd(W)
s_sqrt = numpy.diag(numpy.sqrt(s))
vec_left = u@s_sqrt
vec_right = (s_sqrt@v).T

#compress
vec_left = vec_left[:,:vec_size]
vec_right = vec_right[:,:vec_size]

#save
numpy.savetxt("vector_from.csv", vec_left, delimiter=",")
numpy.savetxt("vector_to.csv", vec_right, delimiter=",")
