#!/usr/bin/env python3

import sys
import numpy
import csv
import pickle
import pandas

#read data
mikolov_test = pandas.read_csv(sys.argv[1], sep=" ", comment=":", header=None)
x=numpy.loadtxt(sys.argv[2], delimiter=",")
with open(sys.argv[3]) as f:
    vocab=f.read().splitlines()

word2ind = {}
for i in range(len(vocab)):
   word2ind[vocab[i]] = i 

#for cosine similarity
x_norm = x/numpy.sqrt(numpy.sum(x**2,axis=1,keepdims=True))

data_count = 0
process_count = 0
correct_count = 0
for idx, data in mikolov_test.iterrows():
    w1 = data[0].lower()
    w2 = data[1].lower()
    w3 = data[2].lower()
    w4 = data[3].lower()
    data_count += 1
    if w1 in vocab and w2 in vocab and w3 in vocab and w4 in vocab:
        n1 = word2ind[w1]
        n2 = word2ind[w2]
        n3 = word2ind[w3]
        n4 = word2ind[w4]
        vec = x[n3,:] + (x[n2,:] - x[n1,:])
        vec_norm = vec/numpy.sqrt(numpy.sum(vec**2))
        cos_sim = numpy.sum(x_norm*vec_norm.reshape((1,len(vec_norm))),axis=1)
        #words in the question were eliminated (Levy & Goldberg, 2014)
        cos_sim[n1]=-1
        cos_sim[n2]=-1
        cos_sim[n3]=-1
        argmax_cos_sim = numpy.argmax(cos_sim)
        print(idx, ": ", w1,w2,w3,"ans:", w4, "predict:",vocab[argmax_cos_sim])
        process_count += 1
        if word2ind[w4] == argmax_cos_sim:
            correct_count += 1
    else:
        print(f"{idx}: {w1} or {w2} or {w3} or {w4} not in vocab. skipped.")

correct_rate = correct_count/process_count
print(f"{process_count}/{data_count} processed. correct rate = {correct_rate} ({correct_count}/{process_count})")
