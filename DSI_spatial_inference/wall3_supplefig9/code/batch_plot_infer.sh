#!/bin/bash

for VEC in A B C
do
    python inference_vectors.py $VEC vector_from.csv vector_from_infer.csv
    python plot_analysis_grid.py vector_from_infer.csv > gridness_results.txt
    mkdir plot_vec_from_${VEC}
    mv rep*.svg grid*.svg gridness_results.txt plot_vec_from_${VEC}

    python inference_vectors.py $VEC vector_goal.csv vector_goal_infer.csv
    python plot_analysis_grid.py vector_goal_infer.csv > gridness_results.txt
    mkdir plot_vec_goal_${VEC}
    mv rep*.svg grid*.svg gridness_results.txt plot_vec_goal_${VEC}
done
