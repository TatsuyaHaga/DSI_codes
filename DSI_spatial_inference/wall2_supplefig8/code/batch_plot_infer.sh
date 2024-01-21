#!/bin/bash

for VEC in A B C
do
    python inference_vectors.py $VEC vector_from.csv vector_from_infer.csv
    #python plot_rep.py vector_from_infer.csv -1
    python plot_gridcells_simple.py vector_from_infer.csv
    mkdir plot_vec_from_${VEC}
    mv rep*.svg plot_vec_from_${VEC}

    python inference_vectors.py $VEC vector_goal.csv vector_goal_infer.csv
    #python plot_rep.py vector_goal_infer.csv -1
    python plot_gridcells_simple.py vector_goal_infer.csv
    mkdir plot_vec_goal_${VEC}
    mv rep*.svg plot_vec_goal_${VEC}
done
