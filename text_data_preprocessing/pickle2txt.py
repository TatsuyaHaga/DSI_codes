#!/usr/bin/env python3

import sys
import pickle
import itertools

with open(sys.argv[1], "rb") as f:
    data=pickle.load(f)

data1d=list(itertools.chain(*data))

#save results
with open(sys.argv[2],"w") as f:
    for x in data1d:
        f.write(x+" ")
