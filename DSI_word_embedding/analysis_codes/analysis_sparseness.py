#!/usr/bin/env python3

import sys
import csv
import numpy

x = numpy.loadtxt(sys.argv[1], delimiter=",")
with open(sys.argv[2]) as f:
    vocab = f.read().splitlines()

#explain_ratio = 0.9
Nsum = 10

#sparseness
result = numpy.zeros(x.shape[0])
for idx in range(x.shape[0]):
    vec = x[idx,:]
    ranked = numpy.sort(vec)
    sum_all = numpy.sum(ranked)
    sum_part = 0.0
    """
    for n in range(1,len(ranked)+1):
        sum_part += ranked[-n]
        if sum_part/sum_all >= explain_ratio:
            count_explain[idx] = n
            break
    """
    for n in range(1,Nsum+1):
        sum_part += ranked[-n]
    result[idx] = sum_part/sum_all
        
numpy.savetxt("explain_ratio.csv", result, delimiter=",")

#output ranking
print(f"AVERAGE,{numpy.mean(result)}")
argsort = numpy.argsort(result)
for ind in argsort:
    print(f"{vocab[ind]},{result[ind]}")

