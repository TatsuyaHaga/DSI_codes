#!/usr/bin/env python

import numpy
import scipy.stats
import matplotlib.pyplot as plt
import scipy.stats

labels = ["DSI(decorr)", "DSI(sparse)", "DSI(non-neg. OFF)", "Skip-gram", "CBOW", "GLoVe", "PPMI-SVD", "SR-SVD"]
fname = ["DSI_decor", "DSI_sparse", "DSI_nonnegOFF", "skip-gram", "CBOW", "glove", "PPMI", "SR-SVD"]
#settings = ["Sparse(1)", "Sparse(2)", "Sparse(3)", "Sparse(4)", "Sparse(5)", "Full vector"]
settings = ["2", "4", "6", "8", "10", "300\n(Full)"]

data = {}
for i,label in enumerate(labels):
    data[label] = numpy.loadtxt("data/"+fname[i]+".csv", delimiter=",")

data_analogy_mean = {}
data_analogy = {}
for label in labels:
    if "DSI" in label:
        data_analogy_mean[label] = numpy.mean(data[label][:,3:], axis=0)
        data_analogy[label] = data[label][:,3:]
    else:
        data_analogy_mean[label] = data[label][3:]
        data_analogy[label] = data[label][3:]

#plot
def plt_setspines():
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().yaxis.set_ticks_position("left")
    plt.gca().xaxis.set_ticks_position("bottom")

plt.figure(figsize=(3.5,3))
plt_setspines()
xpos = numpy.arange(len(settings))+0.5
for label in reversed(labels):
    if label == "DSI(decorr)":
        plt.plot(xpos, data_analogy_mean[label], "-", label=label, color="black")
        for i in range(5):
            plt.plot(xpos+0.03, data_analogy[label][i,:], ".", color="black")
    elif label == "DSI(sparse)":
        plt.plot(xpos, data_analogy_mean[label], "-", label=label, color="lightgray")
        for i in range(5):
            plt.plot(xpos-0.03, data_analogy[label][i,:], ".", color="lightgray")
    elif label == "DSI(non-neg. OFF)":
        plt.plot(xpos, data_analogy_mean[label], "--", label=label, color="gray")
        for i in range(5):
            plt.plot(xpos, data_analogy[label][i,:], ".", color="gray")
    else:
        plt.plot(xpos, data_analogy_mean[label], ".-", label=label)

plt.xticks(xpos, settings)#, rotation="vertical")
plt.xlabel("The number of non-zero elements\n in sparsified vectors")
plt.ylabel("Success rate of\nanalogical inference")
plt.legend()
plt.tight_layout()
plt.savefig("sparse_inference_summary.svg")

#statistical tests
fout = open("stat_test_sparse_inference.txt", "w")

fout.write(f"DSI(decorr) vs DSI(sparse), ttest_ind(two-sided)\n")
for n in range(len(settings)):
    tstat, p = scipy.stats.ttest_ind(data_analogy["DSI(decorr)"][:,n], data_analogy["DSI(sparse)"][:,n])
    fout.write(f"x={n+1}, t={tstat}, p={p}\n")

fout.write(f"\nDSI(decorr) vs DSI(non-neg. OFF), ttest_ind(two-sided)\n")
for n in range(len(settings)):
    tstat, p = scipy.stats.ttest_ind(data_analogy["DSI(decorr)"][:,n], data_analogy["DSI(non-neg. OFF)"][:,n])
    fout.write(f"x={n+1}, t={tstat}, p={p}\n")

fout.write(f"\nDSI(decorr) vs Skip-gram, ttest_1samp(two-sided)\n")
for n in range(len(settings)):
    tstat, p = scipy.stats.ttest_1samp(data_analogy["DSI(decorr)"][:,n], data_analogy["Skip-gram"][n])
    fout.write(f"x={n+1}, t={tstat}, p={p}\n")

fout.write(f"\nDSI(decorr) vs CBOW, ttest_1samp(two-sided)\n")
for n in range(len(settings)):
    tstat, p = scipy.stats.ttest_1samp(data_analogy["DSI(decorr)"][:,n], data_analogy["CBOW"][n])
    fout.write(f"x={n+1}, t={tstat}, p={p}\n")

fout.write(f"\nDSI(decorr) vs GLoVe, ttest_1samp(two-sided)\n")
for n in range(len(settings)):
    tstat, p = scipy.stats.ttest_1samp(data_analogy["DSI(decorr)"][:,n], data_analogy["GLoVe"][n])
    fout.write(f"x={n+1}, t={tstat}, p={p}\n")

fout.write(f"\nDSI(decorr) vs PPMI-SVD, ttest_1samp(two-sided)\n")
for n in range(len(settings)):
    tstat, p = scipy.stats.ttest_1samp(data_analogy["DSI(decorr)"][:,n], data_analogy["PPMI-SVD"][n])
    fout.write(f"x={n+1}, t={tstat}, p={p}\n")

fout.write(f"\nDSI(decorr) vs SR-SVD, ttest_1samp(two-sided)\n")
for n in range(len(settings)):
    tstat, p = scipy.stats.ttest_1samp(data_analogy["DSI(decorr)"][:,n], data_analogy["SR-SVD"][n])
    fout.write(f"x={n+1}, t={tstat}, p={p}\n")

fout.close()
