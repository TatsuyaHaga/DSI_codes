#!/bin/bash

DIR_EVAL=../dataset_eval
VEC=vector
for N_ELEMENT in 1 2 3 4 5
do
    python ${DIR_EVAL}/eval_mikolovdata_sparse.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt ${VEC}.csv words.csv ${N_ELEMENT} > result_mikolovtest_${VEC}_sparse_${N_ELEMENT}.txt
done
