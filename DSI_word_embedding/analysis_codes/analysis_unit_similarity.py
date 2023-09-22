#!/usr/bin/env python3

import sys
import csv
import random
import itertools
import numpy
import scipy.stats

import nltk
nltk.download("wordnet")
nltk.download("omw-1.4")
from nltk.corpus import wordnet

x = numpy.loadtxt(sys.argv[1], delimiter=",")
with open(sys.argv[2]) as f:
    vocab = f.read().splitlines()

Nunit = x.shape[1]
rank_max = 10 #maximum rank to be checked
mincount_in_wordnet = 5
Nrandom = 1000
percentile = 95

#TOP words for each unit
topwords = []
topwords_val = []
for dim in range(Nunit):
    idx_rank = numpy.argsort(x[:,dim])[::-1]
    idx_rank = idx_rank[:rank_max]
    topwords.append([vocab[i] for i in idx_rank])

#Wordnet similarity within each unit
def exist_in_wordnet(words):
    return [w for w in words if len(wordnet.synsets(w))>0]

def get_similarity(w1, w2):
    synsets1 = wordnet.synsets(w1)
    synsets2 = wordnet.synsets(w2)
    if len(synsets1)==0 or len(synsets2)==0:
        return None
    combi = itertools.product(synsets1, synsets2)
    #combi_list = []
    sim_all = []
    for s1, s2 in combi:
        #combi_list.append((s1, s2))
        sim = s1.path_similarity(s2)
        if sim!=None and sim!=numpy.nan:
            sim_all.append(sim)
        #else:
        #    sim_all.append(0.0)
    if len(sim_all)>0:
        return numpy.max(sim_all)
    else:
        return None

print("calculating similarity within units...")
mean_similarity = numpy.zeros(Nunit)
for dim in range(Nunit):
    words_exist = exist_in_wordnet(topwords[dim])
    if len(words_exist) < mincount_in_wordnet:
        mean_similarity[dim] = -1
        print(f"Unit {dim+1}: Not available in wordnet.")
        continue
    similarity = []
    for w1, w2 in itertools.combinations(words_exist, 2):
        tmp = get_similarity(w1, w2)
        if tmp!=None:
            similarity.append(tmp)
    if len(similarity)>0:
        mean_similarity[dim] = numpy.mean(similarity)
    else:
        mean_similarity[dim] = -1
        print(f"Unit {dim+1}: all similarities were None.")

#Wordnet similarity for random word combinations
print("calculating similarity of random words...")
mean_similarity_random = []
while True:
    random_words = random.sample(vocab, rank_max)
    words_exist = exist_in_wordnet(random_words)
    if len(words_exist) < mincount_in_wordnet:
        continue
    similarity = []
    for w1, w2 in itertools.combinations(words_exist, 2):
        tmp = get_similarity(w1, w2)
        if tmp!=None:
            similarity.append(tmp)
    if len(similarity)>0:
        mean_similarity_random.append(numpy.mean(similarity))
    if len(mean_similarity_random)>Nrandom:
        break

thr_sig = numpy.percentile(mean_similarity_random, percentile)
calculated = mean_similarity >= 0
significance = mean_similarity > thr_sig

concept_specificity = mean_similarity / numpy.mean(mean_similarity_random) - 1

print(f"calculated units = {numpy.sum(calculated)} / {Nunit}, significant units={numpy.sum(significance)}, ratio of significant units={numpy.sum(significance)/numpy.sum(calculated)}, significance threshold={thr_sig} ({percentile} percentile in null dist.)")
print("mean similarity")
print(f"All units: mean={numpy.mean(mean_similarity[calculated])}, std={numpy.std(mean_similarity[calculated])}")
print(f"Significant units: mean={numpy.mean(mean_similarity[significance])}, std={numpy.std(mean_similarity[significance])}")
print("concept specificity")
print(f"All units: mean={numpy.mean(concept_specificity[calculated])}, std={numpy.std(concept_specificity[calculated])}")
print(f"Significant units: mean={numpy.mean(concept_specificity[significance])}, std={numpy.std(concept_specificity[significance])}")

print("High similarity unit:", 1+numpy.argsort(mean_similarity)[::-1][:10])

numpy.savetxt("similarity_eachunit.csv", numpy.vstack([mean_similarity, 2*significance-1]).T, delimiter=",")
numpy.savetxt("concept_specificity_eachunit.csv", numpy.vstack([concept_specificity, 2*significance-1]).T, delimiter=",")
