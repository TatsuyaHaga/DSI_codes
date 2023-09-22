#!/bin/bash

python pathintegration_training.py adjacency.csv vector_from.csv 
python pathintegration_test.py adjacency.csv vector_from.csv direction_weight.npy
python pathintegration_test_random.py adjacency.csv vector_from.csv direction_weight.npy > pathintegration_test_random_result.txt
