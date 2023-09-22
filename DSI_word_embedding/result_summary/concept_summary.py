#!/usr/bin/env python

import numpy
import scipy.stats
import matplotlib.pyplot as plt
import scipy.stats

labels = ["DSI(decorr)", "DSI(sparse)", "CBOW", "DSI(non-neg. OFF)", "Skip-gram", "GLoVe", "PPMI-SVD", "SR-SVD", "BERT"]
fname = ["DSI_decor", "DSI_sparse", "CBOW", "DSI_nonnegOFF", "skip-gram", "glove", "PPMI", "SR-SVD", "BERT"]

data = {}
for i,label in enumerate(labels):
    data[label] = numpy.loadtxt("data/"+fname[i]+".csv", delimiter=",")

data_ratio_mean = []
data_ratio_sample = []
data_specificity_mean = []
data_specificity_sample = []
data_similarity_mean = []
data_similarity_sample = []

data_ratio_DSI = []
data_ratio_other = []
data_specificity_DSI = []
data_specificity_other = []
data_similarity_DSI = []
data_similarity_other = []
for i,label in enumerate(labels):
    if "DSI" in label:
        data_ratio_mean.append(numpy.mean(data[label][:,0]))
        data_specificity_mean.append(numpy.mean(data[label][:,1]))
        data_similarity_mean.append(numpy.mean(data[label][:,2]))
        data_ratio_DSI.append(data[label][:,0])
        data_specificity_DSI.append(data[label][:,1])
        data_similarity_DSI.append(data[label][:,2])
    else:
        data_ratio_mean.append(data[label][0])
        data_specificity_mean.append(data[label][1])
        data_similarity_mean.append(data[label][2])
        data_ratio_other.append(data[label][0])
        data_specificity_other.append(data[label][1])
        data_similarity_other.append(data[label][2])

#plot
def plt_setspines():
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().yaxis.set_ticks_position("left")
    plt.gca().xaxis.set_ticks_position("bottom")

plt.figure(figsize=(3.5,3))
plt_setspines()
xpos = numpy.arange(len(labels))+0.5
plt.barh(xpos, data_ratio_mean)
for i in range(5):
    plt.plot(data_ratio_DSI[0][i], xpos[0]+0.1*i-0.25, ".", color="black")
    plt.plot(data_ratio_DSI[1][i], xpos[1]+0.1*i-0.25, ".", color="black")
    plt.plot(data_ratio_DSI[2][i], xpos[3]+0.1*i-0.25, ".", color="black")
plt.yticks(xpos, labels)
plt.xlabel("Ratio of\nconcept-specific units")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("concept_ratio_summary.svg")

plt.figure(figsize=(3.5,3))
plt_setspines()
xpos = numpy.arange(len(labels))+0.5
plt.barh(xpos, data_specificity_mean)
for i in range(5):
    plt.plot(data_specificity_DSI[0][i], xpos[0]+0.1*i-0.25, ".", color="black")
    plt.plot(data_specificity_DSI[1][i], xpos[1]+0.1*i-0.25, ".", color="black")
    plt.plot(data_specificity_DSI[2][i], xpos[3]+0.1*i-0.25, ".", color="black")
plt.yticks(xpos, labels)
plt.xlabel("Average conceptual specificity")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("concept_specificity_summary.svg")

plt.figure(figsize=(4,3))
plt_setspines()
xpos = numpy.arange(len(labels))+0.5
plt.barh(xpos[:-1], data_similarity_mean[:-1])
for i in range(5):
    plt.plot(data_similarity_DSI[0][i], xpos[0]+0.1*i-0.25, ".", color="black")
    plt.plot(data_similarity_DSI[1][i], xpos[1]+0.1*i-0.25, ".", color="black")
    plt.plot(data_similarity_DSI[2][i], xpos[3]+0.1*i-0.25, ".", color="black")
plt.yticks(xpos[:-1], labels[:-1])
plt.xlim([0.5,0.75])
plt.xlabel("Rank correlation between\nvector similarity and human data")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("word_similality_summary.svg")

#statistical analyses
fout = open("stat_tests.txt", "w")

tstat, p = scipy.stats.ttest_ind(data_ratio_DSI[0], data_ratio_DSI[1])
fout.write(f"ratio, DSI(decorr) vs DSI(sparse), ttest_ind(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_ind(data_ratio_DSI[0], data_ratio_DSI[2])
fout.write(f"ratio, DSI(decorr) vs DSI(non-neg. OFF), ttest_ind(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_ratio_DSI[0], data_ratio_other[0])
fout.write(f"ratio, DSI(decorr) vs CBOW, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_ratio_DSI[0], data_ratio_other[1])
fout.write(f"ratio, DSI(decorr) vs Skip-gram, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_ratio_DSI[0], data_ratio_other[2])
fout.write(f"ratio, DSI(decorr) vs GLoVe, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_ratio_DSI[0], data_ratio_other[3])
fout.write(f"ratio, DSI(decorr) vs PPMI-SVD, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_ratio_DSI[0], data_ratio_other[4])
fout.write(f"ratio, DSI(decorr) vs SR-SVD, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_ratio_DSI[0], data_ratio_other[5])
fout.write(f"ratio, DSI(decorr) vs BERT, ttest_1samp(two-sided), t={tstat}, p={p}\n")

fout.write("\n")
tstat, p = scipy.stats.ttest_ind(data_specificity_DSI[0], data_specificity_DSI[1])
fout.write(f"specificity, DSI(decorr) vs DSI(sparse), ttest_ind(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_ind(data_specificity_DSI[0], data_specificity_DSI[2])
fout.write(f"specificity, DSI(decorr) vs DSI(non-neg. OFF), ttest_ind(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_specificity_DSI[0], data_specificity_other[0])
fout.write(f"specificity, DSI(decorr) vs CBOW, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_specificity_DSI[0], data_specificity_other[1])
fout.write(f"specificity, DSI(decorr) vs Skip-gram, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_specificity_DSI[0], data_specificity_other[2])
fout.write(f"specificity, DSI(decorr) vs GLoVe, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_specificity_DSI[0], data_specificity_other[3])
fout.write(f"specificity, DSI(decorr) vs PPMI-SVD, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_specificity_DSI[0], data_specificity_other[4])
fout.write(f"specificity, DSI(decorr) vs SR-SVD, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_specificity_DSI[0], data_specificity_other[5])
fout.write(f"specificity, DSI(decorr) vs BERT, ttest_1samp(two-sided), t={tstat}, p={p}\n")

fout.write("\n")
tstat, p = scipy.stats.ttest_ind(data_similarity_DSI[0], data_similarity_DSI[1])
fout.write(f"similarity, DSI(decorr) vs DSI(sparse), ttest_ind(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_ind(data_similarity_DSI[0], data_similarity_DSI[2])
fout.write(f"similarity, DSI(decorr) vs DSI(non-neg. OFF), t={tstat}, ttest_ind(two-sided), p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_similarity_DSI[0], data_similarity_other[0])
fout.write(f"similarity, DSI(decorr) vs CBOW, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_similarity_DSI[0], data_similarity_other[1])
fout.write(f"similarity, DSI(decorr) vs Skip-gram, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_similarity_DSI[0], data_similarity_other[2])
fout.write(f"similarity, DSI(decorr) vs GLoVe, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_similarity_DSI[0], data_similarity_other[3])
fout.write(f"similarity, DSI(decorr) vs PPMI-SVD, ttest_1samp(two-sided), t={tstat}, p={p}\n")
tstat, p = scipy.stats.ttest_1samp(data_similarity_DSI[0], data_similarity_other[4])
fout.write(f"similarity, DSI(decorr) vs SR-SVD, ttest_1samp(two-sided), t={tstat}, p={p}\n")

fout.close()
