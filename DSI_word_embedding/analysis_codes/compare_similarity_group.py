#!/usr/bin/env python3

import sys
import numpy
import pylab
import itertools

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
meandist_samegroup = 0.0
meandist_diffgroup = 0.0
count_samegroup = 0
count_diffgroup = 0
for i in range(Nword):
    dist_rep[i,i] = 0
for i,j in itertools.combinations(range(Nword), 2):
    dist_rep[i,j] = 1-numpy.corrcoef(rep[i,:], rep[j,:])[0][1]
    dist_rep[j,i] = dist_rep[i,j]
    if (i//Nword_per_group) == (j//Nword_per_group):
        count_samegroup += 1
        meandist_samegroup += dist_rep[i,j]
    else:
        count_diffgroup += 1
        meandist_diffgroup += dist_rep[i,j]

meandist_samegroup = meandist_samegroup / count_samegroup
meandist_diffgroup = meandist_diffgroup / count_diffgroup

print("Mean dissimilarity")
print(f"same group: {meandist_samegroup}")
print(f"different group: {meandist_diffgroup}")
#numpy.savetxt("dist_rep.csv", dist_rep, delimiter=",")

#plot
def plt_setspines():
    pylab.gca().spines["right"].set_visible(False)
    pylab.gca().spines["top"].set_visible(False)
    pylab.gca().yaxis.set_ticks_position("left")
    pylab.gca().xaxis.set_ticks_position("bottom")

pylab.figure(figsize=(4,4))
#pylab.axis("off")
pylab.imshow(dist_rep, interpolation="nearest", aspect="auto", cmap="hot")
#pylab.clim([0,2])
pylab.colorbar()
for i in range(Ngroup):
    tmp = i*Nword_per_group
    pylab.plot([0,Nword], [tmp, tmp], color="black")
    pylab.plot([tmp,tmp], [0, Nword], color="black")

pos = numpy.arange(Ngroup)*Nword_per_group + Nword_per_group/2
pylab.tick_params(length=0)
pylab.xticks(pos, group_name, rotation="vertical")
pylab.yticks(pos, group_name)
pylab.xlim([0, Nword])
pylab.ylim([0, Nword])
pylab.gca().invert_yaxis()
pylab.tight_layout()
pylab.savefig("dissimilarity_word.svg")
pylab.close()
