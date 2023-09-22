#!/usr/bin/env python3

import sys
import numpy
import csv
import pickle
import itertools

x=numpy.loadtxt(sys.argv[1], delimiter=",")
with open(sys.argv[2]) as f: #vocabulary
    vocab=f.read().splitlines()

word2ind = {}
for i in range(len(vocab)):
   word2ind[vocab[i]] = i 

Nshow = 10

word_list = ["berlin","germany","paris","france"]
word_combi_list = [["berlin", "germany"], ["paris", "france"], ["berlin", "paris"], ["germany", "france"]]

#indices are 1-start -> convergion to 0-start
idx_german = 134 - 1
idx_french = 142 - 1
idx_capital = 281 - 1
idx_country = 285 - 1

idx_arr = [idx_german, idx_french, idx_capital, idx_country]
idx_labels = ["German cell", "French cell", "Capital cell", "Country cell"]
vec_arr = []
vec_labels = []

for word1 in word_list:
    idx1 = word2ind[word1]
    print(idx1)
    vec = x[idx1,:]
    vec = vec[idx_arr]
    vec_arr.append(vec)
    vec_labels.append(word1)
    print(word1, vec)

for word1, word2 in word_combi_list:
    idx1=word2ind[word1]
    idx2=word2ind[word2]
    vec=x[idx1,:]-x[idx2,:]
    vec = vec[idx_arr]
    vec_arr.append(vec)
    vec_labels.append(word1+"-"+word2)

import matplotlib.pyplot as plt

plt.figure(figsize=(3,3))
vec_arr = numpy.vstack(vec_arr)
max_vec_arr = numpy.max(numpy.abs(vec_arr))
plt.imshow(vec_arr, interpolation="nearest", aspect="auto", cmap="bwr")
plt.clim([-max_vec_arr, max_vec_arr])
plt.colorbar()
plt.xticks(numpy.arange(len(idx_labels))+0.0, idx_labels, rotation="vertical")
plt.xlabel("Unit (Dimension)")
plt.yticks(numpy.arange(len(vec_labels))+0.0, vec_labels)
plt.ylabel("Vector")
plt.tight_layout()
plt.savefig("plot_argmaxunits.svg")
