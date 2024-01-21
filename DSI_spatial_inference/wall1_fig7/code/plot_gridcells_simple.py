#!/usr/bin/env python3

import numpy
import sys
import matplotlib.pyplot as plt
import pickle
import itertools

rep=numpy.loadtxt(sys.argv[1], delimiter=",")
P,D=rep.shape

G,pos=pickle.load(open("graph.pickle","rb"))
row_max = 0
col_max = 0
for k in pos.keys():
    if pos[k][0]>row_max:
        row_max = pos[k][0]
    if pos[k][1]>col_max:
        col_max = pos[k][1]
row_max += 1
col_max += 1

#2D space representation
rep2D = numpy.zeros([D, row_max, col_max])
for idx in range(D):
    for k in range(P):
        rep2D[idx, pos[k][0], pos[k][1]] = rep[k,idx]

#parameters
max_shift = 18
cor2D_size = 2*max_shift+1

#functions
def calc_cor2D(ratemap):
    global cor2D_size

    #spatial autocorrelation
    cormap = numpy.zeros([cor2D_size, cor2D_size])
    for shift_row, shift_col in itertools.product(range(0, max_shift+1), repeat=2):
        r = ratemap[shift_row:, shift_col:]
        r_shift = ratemap[:row_max-shift_row, :col_max-shift_col]
        cor = numpy.corrcoef(r.reshape(-1), r_shift.reshape(-1))[0,1]
        cormap[max_shift+shift_row, max_shift+shift_col] = cor
        cormap[max_shift-shift_row, max_shift-shift_col] = cor
        r = ratemap[shift_row:, :col_max-shift_col]
        r_shift = ratemap[:row_max-shift_row, shift_col:]
        cor = numpy.corrcoef(r.reshape(-1), r_shift.reshape(-1))[0,1]
        cormap[max_shift-shift_row, max_shift+shift_col] = cor
        cormap[max_shift+shift_row, max_shift-shift_col] = cor
    return cormap

#calc cor2D
cor2D = numpy.zeros([D, cor2D_size, cor2D_size])
for i in range(D):
    cor2D[i, :, :] = calc_cor2D(rep2D[i,:,:])

#plot scale, angles
def plt_setspines():
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().yaxis.set_ticks_position("left")
    plt.gca().xaxis.set_ticks_position("bottom")

#plot grids
for idx in range(D):
    #plot_color_network("rep"+str(idx)+".svg",G,pos,rep[:,idx])
    plt.imshow(rep2D[idx,:,:].T, interpolation="none", cmap="jet")
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.colorbar()
    plt.savefig("rep"+str(idx)+"_2D.svg")
    plt.close()

    plt.imshow(cor2D[idx,:,:].T, interpolation="none", cmap="jet")
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.colorbar()
    plt.savefig("rep"+str(idx)+"_2Dcor.svg")
    plt.close()
