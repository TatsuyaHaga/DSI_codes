#!/usr/bin/env python3

import sys
import numpy
import pandas

data = pandas.read_csv(sys.argv[1], sep=" ", header=None)
vocab = list(data.iloc[:,0])
vec = data.iloc[:,1:].to_numpy()

numpy.savetxt("vector.csv", vec, delimiter=",")
with open("words.csv","w") as f:
    for x in vocab:
        f.write(str(x)+"\n")
