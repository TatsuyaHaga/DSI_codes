#!/usr/bin/env python3

import numpy
import sys
import matplotlib.pyplot as plt
import networkx
import pickle
import itertools

def plt_setspines():
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().yaxis.set_ticks_position("left")
    plt.gca().xaxis.set_ticks_position("bottom")

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

#spatial autocorrelation
max_shift = 15
cor2D_size = 2*max_shift+1
cor2D = numpy.zeros([D, cor2D_size, cor2D_size])
for idx in range(D):
    for shift_row, shift_col in itertools.product(range(0, max_shift+1), repeat=2):
        r = rep2D[idx, shift_row:, shift_col:]
        r_shift = rep2D[idx, :row_max-shift_row, :col_max-shift_col]
        cor = numpy.corrcoef(r.reshape(-1), r_shift.reshape(-1))[0,1]
        cor2D[idx, max_shift+shift_row, max_shift+shift_col] = cor
        cor2D[idx, max_shift-shift_row, max_shift-shift_col] = cor
        r = rep2D[idx, shift_row:, :col_max-shift_col]
        r_shift = rep2D[idx, :row_max-shift_row, shift_col:]
        cor = numpy.corrcoef(r.reshape(-1), r_shift.reshape(-1))[0,1]
        cor2D[idx, max_shift-shift_row, max_shift+shift_col] = cor
        cor2D[idx, max_shift+shift_row, max_shift-shift_col] = cor

#rotation and gridness
gridness = numpy.zeros(D)
degree_arr = [0.0, 30.0, 60.0, 90.0, 120.0, 150.0]
Ndegree = 6
def interpolation(z, val_floor, val_ceil):
    return val_floor + (z-numpy.floor(z))*val_ceil
for idx in range(D):
    r = cor2D[idx, :, :]
    cor_rot = numpy.zeros(Ndegree)
    for i_degree in range(Ndegree):
        rad = numpy.pi * (degree_arr[i_degree]/180.0)
        r_rot = numpy.zeros_like(r)
        r_rot_filter = numpy.ones_like(r)
        for x,y in itertools.product(range(cor2D_size), repeat=2):
            #rotate coordinates
            x_rot = max_shift + numpy.cos(rad)*(x-max_shift) - numpy.sin(rad)*(y-max_shift)
            y_rot = max_shift + numpy.sin(rad)*(x-max_shift) + numpy.cos(rad)*(y-max_shift)
            xceil = int(numpy.ceil(x_rot))
            xfloor = int(numpy.floor(x_rot))
            yceil = int(numpy.ceil(y_rot))
            yfloor = int(numpy.floor(y_rot))
            if xfloor<0 or yfloor<0 or xceil>=cor2D_size or yceil>=cor2D_size:
                r_rot_filter[x,y] = 0
                continue
            #linear interpolation
            interp_yceil = interpolation(x_rot, r[xfloor, yceil], r[xceil, yceil])
            interp_yfloor = interpolation(x_rot, r[xfloor, yfloor], r[xceil, yfloor])
            r_rot[x,y] = interpolation(y_rot, interp_yfloor, interp_yceil)
        cor_rot[i_degree] = numpy.corrcoef((r_rot_filter*r).reshape(-1), r_rot.reshape(-1))[0,1]
    gridness[idx] = numpy.min(cor_rot[[0,2,4]]) - numpy.max(cor_rot[[1,3,5]]) #min(0deg, 60deg, 120deg) - max(30deg, 90deg, 150deg)

is_gridcell = gridness>0.0
numpy.savetxt("gridness_val.csv", gridness, delimiter=",")

