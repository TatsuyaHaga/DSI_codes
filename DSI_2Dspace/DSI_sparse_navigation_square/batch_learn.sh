#!/bin/bash

time python count_successor.py state_seq.csv 0.99
time python compress_sinfo_sparse.py successor_count.npy state_count.csv 100
