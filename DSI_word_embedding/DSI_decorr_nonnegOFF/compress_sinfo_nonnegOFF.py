#!/usr/bin/env python3

import sys
import numpy
import itertools

#inputs
S = numpy.load(sys.argv[1]) #successor counts (row:from, col:to)
C = numpy.loadtxt(sys.argv[2], delimiter=",") #state counts
Dcomp = int(sys.argv[3]) #dimension of compressed representation
Nstate = len(C)

#calculation setting
batchsize = 1024 #to reduce memory comsumption; no effect on results
use_cupy = True #using GPU or not
if use_cupy:
    print("Cupy (gpu) mode.")
    import cupy
else:
    print("Numpy (cpu) mode.")
all_data_GPU = True #transfer whole SI matrix to GPU, large memory comsumption

#parameters
Niterate = 10000
eta = 0.05
decay = 1e-3
decor = 1.0
SImin = 1e-3

#probability and SI
P = C/numpy.sum(C) #state frequency

SI = S / P.reshape((1,len(P)))
SI = numpy.maximum(SI, 1)
SI = numpy.log(SI)
SI = SI.T

SImean = numpy.mean(SI)
SIvar = numpy.var(SI)

print(f"Nstate={Nstate}, Dcomp={Dcomp}")

#switch functions
if use_cupy:
    if all_data_GPU:
        SI = cupy.asarray(SI)

    nc_zeros = cupy.zeros
    nc_zeros_like = cupy.zeros_like
    nc_rand = cupy.random.rand
    nc_eye = cupy.eye
    nc_logical_not = cupy.logical_not
    nc_sum = cupy.sum
    nc_dot = cupy.dot
    nc_diag = cupy.diag
    nc_outer = cupy.outer
    nc_transpose = cupy.transpose
    nc_maximum = cupy.maximum
    nc_mean = cupy.mean
    nc_sqrt = cupy.sqrt
else:
    nc_zeros = numpy.zeros
    nc_zeros_like = numpy.zeros_like
    nc_rand = numpy.random.rand
    nc_eye = numpy.eye
    nc_logical_not = numpy.logical_not
    nc_sum = numpy.sum
    nc_dot = numpy.dot
    nc_diag = numpy.diag
    nc_outer = numpy.outer
    nc_transpose = numpy.transpose
    nc_maximum = numpy.maximum
    nc_mean = numpy.mean
    nc_sqrt = numpy.sqrt
    nc_zeros = numpy.zeros

#matrices
Xfrom = 2*nc_rand(Dcomp, Nstate)*nc_sqrt(SImean/Dcomp)
Xgoal = 2*nc_rand(Nstate, Dcomp)*nc_sqrt(SImean/Dcomp)
deltaXfrom = nc_zeros_like(Xfrom)
deltaXgoal = nc_zeros_like(Xgoal)
covar_diag = nc_eye(Dcomp, dtype=bool)
covar_offdiag = nc_logical_not(covar_diag)

#nestrov
t_nest = 1.0
def nestrov(x):
    return 0.5*(1 + numpy.sqrt(1+4*x*x))

print("compressing representation,", Niterate, "iterations")
for ite in range(Niterate):
    if (ite+1)%100==0:
        display_result = True
    else:
        display_result = False

    #nestrov
    t_nest_prev = t_nest+0.0
    t_nest = nestrov(t_nest)
    momentum = (t_nest_prev-1)/t_nest

    #decorrelation
    demean = Xfrom - nc_sum(Xfrom, axis=1, keepdims=True)/Nstate
    covar = nc_dot(demean, nc_transpose(demean))/Nstate
    var = nc_diag(covar)
    Wcor = covar_offdiag * covar / nc_outer(var, var)
    grad_cor = nc_dot(Wcor, demean/Nstate)

    #error
    err_sum = 0.0
    grad_err_Xgoal = nc_zeros_like(Xgoal)
    grad_err_Xfrom = nc_zeros_like(Xfrom)
    for idx in range(0, Nstate, batchsize):
        #extract parts of data
        idx_end = idx + batchsize
        if idx_end > Nstate:
            idx_end = Nstate
        if use_cupy:
            SIpart = cupy.asarray(SI[:,idx:idx_end])
        else:
            SIpart = SI[:,idx:idx_end]
        #error
        err = SIpart - nc_dot(Xgoal, Xfrom[:,idx:idx_end])
        err_w = (SIpart/SImean+SImin) / (Nstate*SIvar) * err #weighted error
        if display_result:
            err_sum += nc_sum(err_w*err)
        #gradient
        grad_err_Xgoal = grad_err_Xgoal + nc_dot(err_w, nc_transpose(Xfrom[:,idx:idx_end]))
        grad_err_Xfrom[:,idx:idx_end] = nc_dot(nc_transpose(Xgoal), err_w)

    #update matrices
    deltaXgoal = momentum * deltaXgoal + eta * (grad_err_Xgoal - decay*Xgoal)
    deltaXfrom = momentum * deltaXfrom + eta * (grad_err_Xfrom - decay*Xfrom - decor*grad_cor)
    Xgoal = Xgoal + deltaXgoal
    Xfrom = Xfrom + deltaXfrom

    #non-negative constraints
    #Xgoal = nc_maximum(Xgoal, 0)
    #Xfrom = nc_maximum(Xfrom, 0)

    #check objective and output
    if display_result:
        cor_sum = nc_mean(nc_sqrt(Wcor*covar))
        print(f"{ite+1} iteration: err={err_sum/Nstate:.5e}, cor={cor_sum:.5e}")
        
#save
if use_cupy:
    Xfrom = cupy.asnumpy(Xfrom)
    Xgoal = cupy.asnumpy(Xgoal)
numpy.savetxt("vector_from.csv", Xfrom.T, delimiter=",")
numpy.savetxt("vector_goal.csv", Xgoal, delimiter=",")

print("end.")

