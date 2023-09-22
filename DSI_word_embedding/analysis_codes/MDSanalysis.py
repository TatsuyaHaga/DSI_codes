#!/usr/bin/env python3

import sys
import numpy
import pylab
import itertools
from sklearn.manifold import MDS

rep_all = numpy.loadtxt(sys.argv[1], delimiter=",")
with open(sys.argv[2]) as f:
    vocab = f.read().splitlines()

Nstate, Drep = rep_all.shape

#grouped words
Ngroup = 10  
Nword_per_group = 10
Nword = Ngroup * Nword_per_group
group_idx = (numpy.arange(Nword) / Nword_per_group).astype(int)

words = []
words.extend(["dog", "cat", "bull", "bear", "elephant", "fox", "horse", "lion", "rat", "tiger"]) #mammal
words.extend(["building", "church", "theater", "hall", "school", "hotel", "house", "library", "mansion", "palace"]) #building
words.extend(["vehicle", "ambulance", "bike", "aircraft", "bus", "car", "helicopter", "locomotive", "rocket", "ship"]) #vehicle
words.extend(["food", "bread", "cheese", "candy", "rice", "beer", "coffee", "milk", "tea", "wine"]) #food
words.extend(["clothing", "shirt", "hat", "belt", "costume", "dress", "wear", "cap", "coat", "crown"]) #clothing
words.extend(["arm", "bone", "lung", "ear", "eye", "finger", "foot", "hair", "kidney", "leg"]) #body part
words.extend(["computer", "software", "internet", "code", "access", "server", "website", "pc", "node", "portal"]) #computer
words.extend(["feeling", "anger", "anxiety", "comfort", "confusion", "emotion", "enthusiasm", "happiness", "joy", "love"]) #feeling
words.extend(["creator", "architect", "artist", "composer", "designer", "producer", "filmmaker", "photographer", "musician", "painter"]) #creator
words.extend(["husband", "brother", "aunt", "cousin", "daughter", "father", "grandfather", "grandmother", "mother", "sister"]) #relative

group_name = ["mammal", "building", "vehicle", "food", "clothing", "body part", "computer", "feeling", "creator", "relative"]

color_list = ["black", "red", "green", "blue", "chocolate", "cyan", "magenta", "gray", "blueviolet", "darkorange"]

#extract representations
rep = numpy.zeros([Nword, Drep])
for i in range(Nword):
    rep[i,:] = rep_all[vocab.index(words[i]),:]

#distance matrix
def cos_sim(x, y):
    return numpy.sum(x*y) / (numpy.linalg.norm(x) * numpy.linalg.norm(y))
dist_rep = numpy.zeros([Nword, Nword])
for i,j in itertools.combinations(range(Nword), 2):
    dist_rep[i,j] = 1-numpy.corrcoef(rep[i,:], rep[j,:])[0][1]
    dist_rep[j,i] = dist_rep[i,j]

#numpy.savetxt("dist_rep.csv", dist_rep, delimiter=",")

#MDS
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=0)
mds_pos_rep = mds.fit_transform(dist_rep)

#plot
def plt_setspines():
    pylab.gca().spines["right"].set_visible(False)
    pylab.gca().spines["top"].set_visible(False)
    pylab.gca().yaxis.set_ticks_position("left")
    pylab.gca().xaxis.set_ticks_position("bottom")

pylab.figure(figsize=(4,4))
pylab.axis("off")
for i in range(Nword):
    x = mds_pos_rep[i,0]
    y = mds_pos_rep[i,1]
    c = color_list[group_idx[i]]
    pylab.plot(x, y, ".", color=c, markersize=10)

for i in range(Ngroup):
    c = color_list[i]
    pylab.text(0.9, (4-i)*0.15, group_name[i], fontsize=12, color=c)

pylab.xlim([-1, 1.5])
pylab.ylim([-1, 1.5])
pylab.savefig("MDS_word.svg")
pylab.close()
