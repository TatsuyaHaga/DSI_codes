#!/bin/bash

DATA_DIR=../text_data

python PPMI.py ${DATA_DIR}/state_seq.csv 10
python compress_svd.py PPMI.csv 300

DIR_EVAL=../dataset_eval
DIR_ANA=../analysis_codes
VEC=vector_left
python ${DIR_EVAL}/eval_WS353.py ${DIR_EVAL}/wordsim353/combined.csv ${VEC}.csv ${DATA_DIR}/words.csv > result_WS353_${VEC}.txt
python ${DIR_EVAL}/eval_mikolovdata.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt ${VEC}.csv ${DATA_DIR}/words.csv > result_mikolovtest_${VEC}.txt
python ${DIR_ANA}/analysis_vector.py ${VEC}.csv ${DATA_DIR}/words.csv > units_${VEC}.txt
python ${DIR_ANA}/analysis_unit_similarity.py ${VEC}.csv ${DATA_DIR}/words.csv > similarity_eachunit_${VEC}.txt

for N_ELEMENT in 1 2 3 4 5
do
    python ${DIR_EVAL}/eval_mikolovdata_sparse.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt ${VEC}.csv ${DATA_DIR}/words.csv ${N_ELEMENT} > result_mikolovtest_${VEC}_sparse_${N_ELEMENT}.txt
done
