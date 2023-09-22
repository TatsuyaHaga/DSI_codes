#!/bin/bash

python analysis_gridness.py vector_from_C.csv 

CONTEXT=AB
for VEC in AB
do
    for N_ELEMENT in 2 4 6 8 10
    do
        python inference_vectors_sparse_CB_grid.py $VEC vector_from.csv vector_from_infer.csv ${N_ELEMENT} gridness_val.csv > vector_from_maxmin.txt
        python inference_vectors_sparse_CB_grid.py $VEC vector_goal.csv vector_goal_infer.csv ${N_ELEMENT} gridness_val.csv > vector_goal_maxmin.txt
        python evaluate_decisionmaking_wall2.py adjacency_$CONTEXT.csv vector_from_infer.csv vector_goal_infer.csv graph$CONTEXT.pickle > decisionmaking_result.txt
        DIR=navigation_${VEC}_${CONTEXT}_grid_sparse${N_ELEMENT}
        mkdir $DIR
        mv decisionmaking_result.txt decision_making*.svg *_maxmin.txt $DIR
    done
done
