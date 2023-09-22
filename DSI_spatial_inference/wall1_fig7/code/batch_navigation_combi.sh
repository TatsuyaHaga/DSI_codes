#!/bin/bash

for VEC in A B C AB
do
    for CONTEXT in A B AB
    do
        python inference_vectors.py $VEC vector_from.csv vector_from_infer.csv
        python inference_vectors.py $VEC vector_goal.csv vector_goal_infer.csv
        python evaluate_decisionmaking_wall1.py adjacency_$CONTEXT.csv vector_from_infer.csv vector_goal_infer.csv graph$CONTEXT.pickle > decisionmaking_result.txt
        DIR=navigation_${VEC}_${CONTEXT}
        mkdir $DIR
        mv decisionmaking_result.txt decision_making*.svg $DIR
    done
done
