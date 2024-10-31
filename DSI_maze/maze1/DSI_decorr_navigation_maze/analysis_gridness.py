#!/usr/bin/env python3

import numpy
import sys
import matplotlib.pyplot as plt
import pickle
import itertools

import scipy
import skimage

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
min_radius = 8
central_peak_max_size = min_radius - 1
min_gridness = 0.3
Nshuffle = 100
sigma_watershed = 1.5
plot_shufflemap = False

max_shuffle = 1000 #if gridness=nan in shuffling, map is reshuffled.

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

def interpolation(z, val_floor, val_ceil):
    return val_floor + (z-numpy.floor(z))*val_ceil

def calc_inner_radius(r): 
    global max_shift
    global central_peak_max_size

    #central peak area -> inner radius
    mean_cor = numpy.zeros(max_shift)
    Nsummed = numpy.zeros_like(mean_cor)
    for x,y in itertools.product(range(cor2D_size), repeat=2):
        dist = numpy.sqrt((x-max_shift)**2 + (y-max_shift)**2)
        idx = int(numpy.floor(dist))
        if idx < max_shift:
            Nsummed[idx] += 1
            mean_cor[idx] += r[x,y]
    mean_cor = mean_cor / Nsummed
    minima_or_negative = ((mean_cor < numpy.roll(mean_cor, -1)) * (mean_cor < numpy.roll(mean_cor, 1))) + (mean_cor < 0)
    if numpy.any(minima_or_negative[1:-1]):
        radius_inner = numpy.where(minima_or_negative[1:-1])[0][0] + 1
    else:
        radius_inner = central_peak_max_size
    
    if radius_inner>central_peak_max_size:
        radius_inner = central_peak_max_size
    #print(radius_inner, flush=True)
    
    return radius_inner

def calc_gridness(r):
    global cor2D_size
    global max_shift
    global min_radius

    radius_inner = calc_inner_radius(cormap)
    #calculate gridness
    degree_arr = [0.0, 30.0, 60.0, 90.0, 120.0, 150.0]
    Ndegree = 6
    radius_arr = numpy.arange(min_radius, max_shift+1)
    Nradius = len(radius_arr)

    cor_rot = numpy.zeros([Nradius, Ndegree])
    for i_degree in range(Ndegree):
        rad = numpy.pi * (degree_arr[i_degree]/180.0)
        r_rot = numpy.zeros_like(r)

        for x,y in itertools.product(range(cor2D_size), repeat=2):
            #rotate coordinates
            x_rot = max_shift + numpy.cos(rad)*(x-max_shift) - numpy.sin(rad)*(y-max_shift)
            y_rot = max_shift + numpy.sin(rad)*(x-max_shift) + numpy.cos(rad)*(y-max_shift)
            xceil = int(numpy.ceil(x_rot))
            xfloor = int(numpy.floor(x_rot))
            yceil = int(numpy.ceil(y_rot))
            yfloor = int(numpy.floor(y_rot))
            if xfloor<0 or yfloor<0 or xceil>=cor2D_size or yceil>=cor2D_size:
                continue
            #linear interpolation
            interp_yceil = interpolation(x_rot, r[xfloor, yceil], r[xceil, yceil])
            interp_yfloor = interpolation(x_rot, r[xfloor, yfloor], r[xceil, yfloor])
            r_rot[x,y] = interpolation(y_rot, interp_yfloor, interp_yceil)

        #calculation of correlation, expanding outer radius
        for i_radius, radius in enumerate(radius_arr):
            r_sample = []
            r_rot_sample = []
            for x,y in itertools.product(range(cor2D_size), repeat=2):
                dist = numpy.sqrt((x-max_shift)**2 + (y-max_shift)**2)
                if dist >= radius_inner and dist <= radius:
                    r_sample.append(r[x,y])
                    r_rot_sample.append(r_rot[x,y])
            cor_rot[i_radius, i_degree] = numpy.corrcoef(r_sample, r_rot_sample)[0,1]

    gridness_radius = numpy.min(cor_rot[:, [0,2,4]], axis=1) - numpy.max(cor_rot[:, [1,3,5]], axis=1) # min(0deg, 60deg, 120deg) - max(30deg, 90deg, 150deg)
    return numpy.max(gridness_radius)

def segment_watershed(r):
    global sigma_watershed
    global plot_shufflemap

    #segmentation by watershed algorithm
    r_gauss = skimage.filters.gaussian(r, sigma=sigma_watershed)
    image = (r_gauss > skimage.filters.threshold_otsu(r_gauss)) #binarized image
    distance = scipy.ndimage.distance_transform_edt(image)
    coords = skimage.feature.peak_local_max(distance, footprint=numpy.ones((3, 3)), labels=image)
    mask = numpy.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = scipy.ndimage.label(mask)
    labels = skimage.segmentation.watershed(-distance, markers, mask=image)
    Nlabel = numpy.max(labels)
    peaks = [[-1, -1]] # background = index 0
    for i in range(1, Nlabel):
        peak = numpy.unravel_index(numpy.argmax(r_gauss*(labels==i)), r.shape)
        peaks.append(tuple(peak))

    if plot_shufflemap:
        plt.figure(figsize=(9,3))
        plt.subplot(1,3,1)
        plt.imshow(r_gauss, interpolation="none")
        plt.subplot(1,3,2)
        plt.imshow(image)
        plt.subplot(1,3,3)
        plt.imshow(labels)
        for i in range(1, len(peaks)):
            plt.plot(peaks[i][1], peaks[i][0], ".")
        plt.show()
        plt.close()

    return labels, peaks

def shuffle_map(ratemap):
    global plot_shufflemap

    x_max, y_max = ratemap.shape

    #segmentation
    segments, peaks = segment_watershed(ratemap)
    Nseg = len(peaks)-1
    segment_order = numpy.random.permutation(Nseg) + 1

    # field shuffling (Barry and Burgess, 2017)
    ratemap_shuffle = numpy.zeros_like(ratemap)
    occupied = numpy.zeros_like(ratemap, dtype=bool)
    for idx_seg in segment_order:
        points_x, points_y = numpy.where(segments==idx_seg) # points in the segment
        peak_orig = peaks[idx_seg] # original peak
        diff_x = points_x - peak_orig[0]
        diff_y = points_y - peak_orig[1]
        points_order = numpy.argsort(numpy.sqrt( diff_x**2 + diff_y**2 )) # points were sorted by distances from the peak

        # random sampling of target peak position (keeping fields inside the area)
        peak_moved = (numpy.random.randint(numpy.max(-diff_x), x_max-numpy.max(diff_x)), numpy.random.randint(numpy.max(-diff_y), y_max-numpy.max(diff_y)))
        #peak_moved = (numpy.random.randint(x_max), numpy.random.randint(y_max))
        while occupied[peak_moved[0], peak_moved[1]]:
            peak_moved = (numpy.random.randint(x_max), numpy.random.randint(y_max))

        #copying points (bins)
        for idx_pt in points_order:
            pt_x = points_x[idx_pt]
            pt_y = points_y[idx_pt]
            pt_moved_x = peak_moved[0] + (pt_x - peak_orig[0])
            pt_moved_y = peak_moved[1] + (pt_y - peak_orig[1])

            if  pt_moved_x<0 or pt_moved_x>=x_max or pt_moved_y<0 or pt_moved_y>=y_max or occupied[pt_moved_x][pt_moved_y]:
                #point occupied or out of the map -> the closest point is chosen
                points_free_x, points_free_y = numpy.where(occupied==False) #unoccupied points
                closest_point = numpy.argmin(numpy.sqrt( (points_free_x - pt_moved_x)**2 + (points_free_y - pt_moved_y)**2 ))
                pt_moved_x = points_free_x[closest_point]
                pt_moved_y = points_free_y[closest_point]
            #bin copied
            ratemap_shuffle[pt_moved_x, pt_moved_y] = ratemap[pt_x, pt_y]
            occupied[pt_moved_x, pt_moved_y] = True

    if plot_shufflemap:
        plt.figure(figsize=(9,3))
        plt.subplot(1,3,1)
        plt.imshow(ratemap, interpolation="none")
        plt.subplot(1,3,2)
        plt.imshow(occupied, interpolation="none")
        plt.subplot(1,3,3)
        plt.imshow(ratemap_shuffle, interpolation="none")
        plt.show()
        plt.close()

    return ratemap_shuffle

#calc cor2D
cor2D = numpy.zeros([D, cor2D_size, cor2D_size])
for i in range(D):
    cor2D[i, :, :] = calc_cor2D(rep2D[i,:,:])

#evaluation of gridness
gridness = numpy.zeros(D)
is_gridcell = numpy.zeros(D, dtype=bool)
print("Unit #, gridness > threshold, True or False")
for idx in range(D):
    cormap = cor2D[idx, :, :]
    gridness[idx] = calc_gridness(cormap)
    if numpy.isnan(gridness[idx]) or gridness[idx]<min_gridness:
        is_gridcell[idx] = False
        print(idx, gridness[idx], is_gridcell[idx], flush=True)
    else:
        ratemap = rep2D[idx, :, :]
        gridness_shuffle = numpy.zeros(Nshuffle)
        gridness_shuffle[:] = numpy.nan
        shuffled = 0
        for s in range(Nshuffle):
            while numpy.isnan(gridness_shuffle[s]):
                ratemap_shuffle = shuffle_map(ratemap)
                cormap_shuffle = calc_cor2D(ratemap_shuffle)
                gridness_shuffle[s] = calc_gridness(cormap_shuffle)
                shuffled += 1
                if shuffled > max_shuffle:
                    break
            if shuffled > max_shuffle:
                break
        if numpy.nan in gridness_shuffle:
            gridness_threshold = numpy.nan
            is_gridcell[idx] = False
        else:
            gridness_threshold = numpy.percentile(gridness_shuffle, 95)
            is_gridcell[idx] = (gridness[idx] > gridness_threshold)
        print(idx, gridness[idx], ">", gridness_threshold, is_gridcell[idx], flush=True)

numpy.savetxt("gridness.csv", gridness, delimiter=",")
numpy.savetxt("is_gridcell.csv", is_gridcell, delimiter=",", fmt="%d")
print("grid cell ratio:", 100*numpy.sum(is_gridcell) / D, "%")
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
    grid_orient_mean[idx] = numpy.mean(tmp)
    tmp = numpy.hstack([peak_angle, peak_angle-90, peak_angle-180, peak_angle-270])
    grid_orient_mintowall[idx] = numpy.min(numpy.abs(tmp))
    grid_orient_all.append(peak_angle)

numpy.savetxt("grid_scale.csv", grid_scale, delimiter=",")
