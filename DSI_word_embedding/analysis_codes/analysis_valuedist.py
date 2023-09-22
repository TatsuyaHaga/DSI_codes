#!/usr/bin/env python3

import sys
import csv
import numpy
import matplotlib.pyplot as plt

x = numpy.loadtxt(sys.argv[1], delimiter=",")

def plt_setspines():
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().yaxis.set_ticks_position("left")
    plt.gca().xaxis.set_ticks_position("bottom")
    
#sorted and scaled values 
plt.figure(figsize=(3,3))
plt_setspines()
vec_sort_avg = numpy.zeros(x.shape[1])
ymax = 0.0
for idx in range(x.shape[0]):
    vec = x[idx,:] / numpy.sum(x[idx,:])
    vec_sort = numpy.sort(vec)[::-1]
    vec_sort_avg = vec_sort_avg + vec_sort
    plt.plot(vec_sort, color="gray")
    if numpy.max(vec_sort)>ymax:
        ymax = numpy.max(vec_sort)

vec_sort_avg = vec_sort_avg / x.shape[0]
plt.plot(range(1, x.shape[1]+1), vec_sort_avg, color="black")
plt.xlabel("Sorted dimension")
plt.ylabel("Ratio of each element\nto sum of all elements")
plt.ylim([0,ymax])
plt.tight_layout()
plt.savefig("valuedist_eachvec.svg")
plt.close()

#each unit
plt.figure(figsize=(3,3))
plt_setspines()
vec_sort_avg = numpy.zeros(x.shape[0])
for idx in range(x.shape[1]):
    vec = x[:,idx] / numpy.max(x[:,idx])
    vec_sort = numpy.sort(vec)[::-1]
    vec_sort_avg = vec_sort_avg + vec_sort
    plt.plot(vec_sort, color="gray")

vec_sort_avg = vec_sort_avg / x.shape[1]
plt.plot(vec_sort_avg, color="black")
plt.xlabel("Sorted state (word)")
plt.ylabel("Scaled value")
plt.xlim([0,500])
plt.tight_layout()
plt.savefig("valuedist_eachunit.svg")
plt.close()

