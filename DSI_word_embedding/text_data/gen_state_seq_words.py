#!/usr/bin/env python3

import sys
import pickle
import nltk
import numpy
import itertools

with open(sys.argv[1], "rb") as f:
    data=pickle.load(f)
min_count = int(sys.argv[2])

Ndata=len(data)
data1d=list(itertools.chain(*data))
wordcount_all = len(data1d)
data1d=list(itertools.chain(*data))
vocab=sorted(set(data1d))
Nvocab=len(vocab)

print("data including", Ndata, "articles,", wordcount_all, "tokens,", Nvocab, "words", flush=True)

#replace non-frequent words
if min_count>1:
    wordcount = nltk.FreqDist(data1d)
    for n in range(Ndata):
        for idx, w in enumerate(data[n]):
            if wordcount[w]<min_count:
                data[n][idx] = "<unk>"

data1d=list(itertools.chain(*data))
vocab=sorted(set(data1d))
Nvocab=len(vocab)
print("min_count=", min_count, "vocabulary reduced to", Nvocab)

#indexing words
n=0
word2ind=dict([])
for w in vocab:
    word2ind[w]=n
    n+=1

#state sequence
print("Generating a state sequence...")
Nread=0
state_seq = []
data_order = range(Ndata)
for data_samp in data_order:
    t = data[data_samp]
    Nread+=1
    if Nread%10000==0:
        print(Nread, "articles completed.", flush=True)
    for w in t:
        n_new=word2ind[w]
        if n_new>=0:
            state_seq.append(n_new)
    state_seq.append(-1) #end of episode
print("end.")

#save results
with open("words.csv","w") as f:
    for x in vocab:
        f.write(x+"\n")
numpy.savetxt("state_seq.csv", state_seq, delimiter=",", fmt="%d")

