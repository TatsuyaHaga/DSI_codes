#!/usr/bin/env python3

import sys
import numpy
import csv
import pickle
import itertools

Nshow=10

x=numpy.loadtxt(sys.argv[1], delimiter=",")
with open(sys.argv[2]) as f: #vocabulary
    vocab=f.read().splitlines()

word2ind = {}
for i in range(len(vocab)):
   word2ind[vocab[i]] = i 

Nshow = 10

word_list = ["berlin","germany","paris","france"]
word_combi_list = itertools.combinations(word_list, 2)

for word1 in word_list:
    idx1=word2ind[word1]
    vec=x[idx1,:]
    print(word1, "large units", 1+numpy.argsort(vec)[-Nshow:])

for word1, word2 in word_combi_list:
    idx1=word2ind[word1]
    idx2=word2ind[word2]
    vec=numpy.abs(x[idx1,:]-x[idx2,:])
    print(word1, "-", word2, "large units", 1+numpy.argsort(vec)[-Nshow:])
