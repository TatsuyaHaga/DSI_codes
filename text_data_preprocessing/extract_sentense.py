#!/usr/bin/env python3

import sys
import pickle
import nltk
import numpy
import itertools

with open(sys.argv[1], "rb") as f:
    data=pickle.load(f)

data_select=int(sys.argv[2])

Ndata=len(data)
data1d=list(itertools.chain(*data))

t = data[data_select]
wordcount_all=len(t)
wordcount=nltk.FreqDist(t)
vocab=sorted(set(t))
Nvocab=len(vocab)

print("article No.", data_select, ",", len(t), "tokens", Nvocab, "words")
print(*t)
