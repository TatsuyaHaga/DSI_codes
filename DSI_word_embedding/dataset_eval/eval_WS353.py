#!/usr/bin/env python3

import sys
import numpy
import csv
import pickle
import pandas
import scipy.stats

#read data
ws353 = pandas.read_csv(sys.argv[1])
x=numpy.loadtxt(sys.argv[2], delimiter=",") #representation vectors
with open(sys.argv[3]) as f: #vocabulary data
    vocab=f.read().splitlines()

word2ind = {}
for i in range(len(vocab)):
   word2ind[vocab[i]] = i 

#for cosine similarity
x_norm = x/numpy.sqrt(numpy.sum(x**2,axis=1,keepdims=True))

#get correlation and cos-sim
arr_cor_human = []
arr_cos_sim = []
data_count = 0
process_count = 0
for idx, data in ws353.iterrows():
    w1 = data[0]
    w2 = data[1]
    cval = data[2]
    data_count += 1
    if (w1 in vocab) and (w2 in vocab):
        cos_sim = numpy.sum(x_norm[word2ind[w1]] * x_norm[word2ind[w2]])
        arr_cor_human.append(cval)
        arr_cos_sim.append(cos_sim)
        process_count += 1
    else:
        print(f"{w1} or {w2} not in vocab. skipped.")

cor_result, pval_result = scipy.stats.spearmanr(arr_cor_human, arr_cos_sim)
print(f"{process_count}/{data_count} pairs processed. Spearman's rho with WS353 = {cor_result}, p={pval_result}")
