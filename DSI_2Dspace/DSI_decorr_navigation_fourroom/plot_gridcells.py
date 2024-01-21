#!/usr/bin/env python3

import numpy
import sys
import matplotlib.pyplot as plt
import pickle
import itertools

rep=numpy.loadtxt(sys.argv[1], delimiter=",")
P,D=rep.shape

gridness = numpy.loadtxt("gridness.csv", delimiter=",")
is_gridcell = (numpy.loadtxt("is_gridcell.csv", delimiter=",", dtype=int) > 0)
grid_scale = numpy.loadtxt("grid_scale.csv", delimiter=",")

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

#KSD analysis
pitch_scale_KSD = 0.1
sigma_scale_KSD = 1.0

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

grid_scale_part = grid_scale[is_gridcell]

#kernel smoothed density estimation & peak detection
scale_KSD_bins = numpy.arange(numpy.min(grid_scale[is_gridcell])-3.0, numpy.max(grid_scale[is_gridcell])+3.0, pitch_scale_KSD)
scale_KSD_density = numpy.zeros_like(scale_KSD_bins)

for idx in range(D):
    if is_gridcell[idx]:
        scale_KSD_density = scale_KSD_density + numpy.exp(-(scale_KSD_bins-grid_scale[idx])**2/(2*sigma_scale_KSD**2)) #/ numpy.sqrt(2*numpy.pi* (sigma_scale_KSD)**2)
scale_KSD_density = scale_KSD_density / numpy.sum(scale_KSD_density)

peakpos_scale_KSD = numpy.where((scale_KSD_density>numpy.roll(scale_KSD_density,1)) * (scale_KSD_density>numpy.roll(scale_KSD_density,-1)))[0]

#plot scale, angles
def plt_setspines():
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().yaxis.set_ticks_position("left")
    plt.gca().xaxis.set_ticks_position("bottom")

plt.hist(grid_scale_part, bins=20, density=True)
plt.xlabel("Grid scale")
plt.savefig("grid_scale_hist.svg")
plt.close()

plt.figure(figsize=(3,3))
plt_setspines()
plt.plot(scale_KSD_bins, scale_KSD_density, color="black")
ymax = 0.01*numpy.ceil(100*numpy.max(scale_KSD_density))
for peak in peakpos_scale_KSD:
    x = scale_KSD_bins[peak]
    y = scale_KSD_density[peak]
    plt.plot([x,x], [0,y], "--", color="red")
    plt.text(x, y+ymax/100, f"{numpy.around(x,decimals=1):.1f}", color="red")
plt.ylim([0.0, ymax])
plt.yticks([0.0, ymax])
plt.xlabel("Grid scale")
plt.ylabel("Prob.")
#plt.ylabel("Counts")
plt.tight_layout()
plt.savefig("grid_scale_KSD.svg")
plt.close()

#plot grids
for idx in range(D):
    if is_gridcell[idx]:
        title = f"Grid cell, gridness={gridness[idx]:.3f}, scale={grid_scale[idx]:.3f}"
    else:
        title = f"Non-grid cell, gridness={gridness[idx]:.3f}"
    #plot_color_network("rep"+str(idx)+".svg",G,pos,rep[:,idx])
    plt.imshow(rep2D[idx,:,:].T, interpolation="none", cmap="jet")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.colorbar()
    plt.savefig("rep"+str(idx)+"_2D.svg")
    plt.close()

    plt.imshow(cor2D[idx,:,:].T, interpolation="none", cmap="jet")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.colorbar()
    plt.savefig("rep"+str(idx)+"_2Dcor.svg")
    plt.close()
