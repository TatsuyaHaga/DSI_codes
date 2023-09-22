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
#numpy.savetxt("gridness.csv", gridness, delimiter=",")
print("gridcell ratio:", 100*numpy.sum(is_gridcell)/D, "%")
print("High gridness score:", numpy.argsort(gridness)[:-11:-1])
print("Low gridness score:", numpy.argsort(gridness)[:10])

#peak detection -> scale and orientation
grid_scale = numpy.zeros(D)
grid_orient_mean = numpy.zeros(D)
grid_orient_mintowall = numpy.zeros(D)
grid_orient_all = []
peak_pos_arr=[]
for idx in range(D):
    if not is_gridcell[idx]:
        peak_pos_arr.append([])
        grid_orient_all.append([])
        continue
    r = cor2D[idx, :, :]
    #peak = local maxima
    ispeak = r>0
    ispeak[max_shift, max_shift] = False
    for x,y in itertools.product([-1,0,1], repeat=2):
        if x!=0 or y!=0:
            ispeak = ispeak * (r>=numpy.roll(r,(x,y),axis=(0,1)))
    #distance and angle of peaks
    Npeak = numpy.sum(ispeak)
    peak_pos = numpy.where(ispeak)
    peak_dist = numpy.zeros(Npeak)
    peak_angle = numpy.zeros(Npeak)
    for n in range(Npeak):
        x = peak_pos[1][n] - max_shift #columns = x-axis
        y = -(peak_pos[0][n] - max_shift) #inverted rows = y-axis
        peak_dist[n] = numpy.sqrt(x**2+y**2)
        peak_angle[n] = 180+numpy.arctan2(y,x)*180/numpy.pi #0 - 360 degree
    #six closest peaks
    hex_arg = numpy.argsort(peak_dist)[:6]
    hex_pos_x = peak_pos[0][hex_arg]
    hex_pos_y = peak_pos[1][hex_arg]
    peak_dist = peak_dist[hex_arg]
    peak_angle = peak_angle[hex_arg]
    #results
    peak_pos_arr.append((hex_pos_x, hex_pos_y))
    grid_scale[idx] = numpy.mean(peak_dist)
    tmp = peak_angle%60
    #tmp[tmp>30] = tmp[tmp>30] - 60.0
    grid_orient_mean[idx] = numpy.mean(tmp)
    tmp = numpy.hstack([peak_angle, peak_angle-90, peak_angle-180, peak_angle-270])
    grid_orient_mintowall[idx] = numpy.min(numpy.abs(tmp))
    grid_orient_all.append(peak_angle)

#numpy.savetxt("grid_scale.csv", grid_scale, delimiter=",")
#numpy.savetxt("grid_orient.csv", grid_orient, delimiter=",")

#kernel smoothed density estimation & peak detection
pitch_scale_KSD = 0.1
sigma_scale_KSD = 1.0
pitch_orient_KSD = 1.0
kappa_orient_KSD = 20.0

scale_KSD_bins = numpy.arange(numpy.min(grid_scale[is_gridcell])-3.0, numpy.max(grid_scale[is_gridcell])+3.0, pitch_scale_KSD)
orient_KSD_bins = numpy.arange(0.0, 360.0, pitch_orient_KSD)
scale_KSD_density = numpy.zeros_like(scale_KSD_bins)
orient_KSD_density = numpy.zeros_like(orient_KSD_bins)

for idx in range(D):
    if is_gridcell[idx]:
        scale_KSD_density = scale_KSD_density + numpy.exp(-(scale_KSD_bins-grid_scale[idx])**2/(2*sigma_scale_KSD**2))
        for sample in grid_orient_all[idx]:
            angle_diff = numpy.pi*(orient_KSD_bins-sample)/180
            orient_KSD_density = orient_KSD_density + numpy.exp(kappa_orient_KSD*numpy.cos(angle_diff))
scale_KSD_density = scale_KSD_density / numpy.sum(scale_KSD_density)
orient_KSD_density = orient_KSD_density / numpy.sum(orient_KSD_density)

peakpos_scale_KSD = numpy.where((scale_KSD_density>numpy.roll(scale_KSD_density,1)) * (scale_KSD_density>numpy.roll(scale_KSD_density,-1)))[0]
peakpos_orient_KSD = numpy.where((orient_KSD_density>numpy.roll(orient_KSD_density,1)) * (orient_KSD_density>numpy.roll(orient_KSD_density,-1)))[0]

#plot scale, angles
plt.plot(numpy.sort(grid_scale[is_gridcell]), ".", color="black")
plt.xlabel("Sorted units")
plt.ylabel("Grid scale")
plt.savefig("grid_scale.svg")
plt.close()
plt.hist(grid_scale[is_gridcell], bins=20)
plt.xlabel("Grid scale")
plt.savefig("grid_scale_hist.svg")
plt.close()
plt.plot(numpy.sort(grid_orient_mean[is_gridcell]), ".", color="black")
plt.xlabel("Sorted units")
plt.ylabel("Mean grid orientation")
plt.savefig("grid_orient.svg")
plt.close()
plt.hist(grid_orient_mean[is_gridcell], bins=20)
plt.xlabel("Mean grid orientation")
plt.savefig("grid_orient_hist.svg")
plt.close()

plt.figure(figsize=(3,3))
plt_setspines()
n, bins, patches = plt.hist(grid_orient_mintowall[is_gridcell], bins=20)
mean = numpy.mean(grid_orient_mintowall[is_gridcell])
plt.plot([mean, mean], [0.0, numpy.max(n)], "--", color="red")
plt.text(mean+0.1, 0.9*numpy.max(n), f"mean={mean:.1f}", color="red")
plt.xlabel("Minimum orientation \nrelative to wall [deg]")
plt.ylabel("Number of units")
plt.tight_layout()
plt.savefig("grid_orient_wall_hist.svg")
plt.close()

plt.figure(figsize=(3,3))
plt_setspines()
plt.plot(scale_KSD_bins, scale_KSD_density, color="black")
ymax = 0.01*numpy.ceil(100*numpy.max(scale_KSD_density))
for n in range(1,5):
    x = 30 / (numpy.sqrt(2))**n
    plt.plot([x,x], [0,ymax], "--", color="blue")
    if n==1:
        plt.text(x, 0.9*ymax, r"$\frac{30}{\sqrt{2}^n}$", color="blue")
for peak in peakpos_scale_KSD:
    x = scale_KSD_bins[peak]
    y = scale_KSD_density[peak]
    plt.plot([x,x], [0,y], "--", color="red")
    plt.text(x, y+ymax/100, f"{numpy.around(x,decimals=1):.1f}", color="red")
plt.ylim([0.0, ymax])
plt.yticks([0.0, ymax])
plt.xlabel("Grid scale")
plt.ylabel("Prob.")
plt.tight_layout()
plt.savefig("grid_scale_KSD.svg")
plt.close()

plt.figure(figsize=(3,3))
plt_setspines()
plt.plot(orient_KSD_bins, orient_KSD_density, color="black")
ymax = 0.001*numpy.ceil(1000*numpy.max(orient_KSD_density))
for angle in [0, 90, 180, 270, 360]:
    plt.plot([angle,angle], [0,ymax], "--", color="blue")
    if angle==00:
        plt.text(angle+1, 0.9*ymax, "Wall", color="blue")
for peak in peakpos_orient_KSD:
    x = orient_KSD_bins[peak]
    y = orient_KSD_density[peak]
    plt.plot([x,x], [0,y], "--", color="red")
plt.ylim([0.0, ymax])
plt.yticks([0.0, ymax])
plt.xlabel("Grid orientation")
plt.ylabel("Prob.")
plt.tight_layout()
plt.savefig("grid_orient_KSD.svg")
plt.close()

#plot grids
for idx in range(D):
    if is_gridcell[idx]:
        title = f"gridness={gridness[idx]:.3f}, scale={grid_scale[idx]:.3f}, mean orientation={grid_orient_mean[idx]:.3f}"
    else:
        title = f"gridness={gridness[idx]:.3f}"
    plt.imshow(rep2D[idx,:,:].T, interpolation="none", cmap="jet")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.colorbar()
    plt.savefig("rep"+str(idx)+"_2D.svg")
    plt.close()

    plt.imshow(cor2D[idx,:,:].T, interpolation="none", cmap="jet")
    if is_gridcell[idx]:
        peak_pos = peak_pos_arr[idx]
        for n in range(len(peak_pos[1])):
            plt.plot([max_shift, peak_pos[0][n]], [max_shift, peak_pos[1][n]], color="black")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.colorbar()
    plt.savefig("rep"+str(idx)+"_2Dcor.svg")
    plt.close()
