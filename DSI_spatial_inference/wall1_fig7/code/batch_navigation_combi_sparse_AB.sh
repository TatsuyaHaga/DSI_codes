#!/bin/bash

CONTEXT=AB
VEC=AB
for N_ELEMENT in 2 4 6 8 10
do
    python inference_vectors_sparse_CB.py $VEC vector_from.csv vector_from_infer.csv ${N_ELEMENT} > vector_from_maxmin.txt
    python inference_vectors_sparse_CB.py $VEC vector_goal.csv vector_goal_infer.csv ${N_ELEMENT} > vector_goal_maxmin.txt
    python evaluate_decisionmaking_wall1.py adjacency_$CONTEXT.csv vector_from_infer.csv vector_goal_infer.csv graph$CONTEXT.pickle > decisionmaking_result.txt
    DIR=navigation_${VEC}_${CONTEXT}_sparse${N_ELEMENT}
    mkdir $DIR
    mv decisionmaking_result.txt decision_making*.svg *_maxmin.txt $DIR
done
