#!/usr/bin/env python3

import sys
import csv
import numpy

x = numpy.loadtxt(sys.argv[1], delimiter=",")
with open(sys.argv[2]) as f:
    vocab = f.read().splitlines()

rank_max = 10 #maximum rank to be checked

#count and output ranking
for dim in range(x.shape[1]):
    print(f"Unit {dim+1}")
    rank = numpy.argsort(x[:,dim])
    for i in range(rank_max):
        ind = rank[-(i+1)]
        print(vocab[ind], x[ind,dim])
    print("")
