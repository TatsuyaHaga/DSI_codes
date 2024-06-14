#!/bin/bash

DATA_DIR=../text_data
time python compress_sinfo.py ${DATA_DIR}/successor_count.npy ${DATA_DIR}/state_count.csv 300

DIR_EVAL=../dataset_eval
DIR_ANA=../analysis_codes
VEC=vector_from

python ${DIR_EVAL}/eval_WS353.py ${DIR_EVAL}/wordsim353/combined.csv ${VEC}.csv ${DATA_DIR}/words.csv > result_WS353_${VEC}.txt
python ${DIR_EVAL}/eval_mikolovdata.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt ${VEC}.csv ${DATA_DIR}/words.csv > result_mikolovtest_${VEC}.txt
python ${DIR_ANA}/analysis_vector.py ${VEC}.csv ${DATA_DIR}/words.csv > units_${VEC}.txt
python ${DIR_ANA}/analysis_sparseness.py ${VEC}.csv ${DATA_DIR}/words.csv > explain_ratio_rank.txt
python ${DIR_ANA}/analysis_valuedist.py ${VEC}.csv 
python ${DIR_ANA}/analysis_unit_similarity.py ${VEC}.csv ${DATA_DIR}/words.csv > similarity_eachunit_${VEC}.txt
python ${DIR_ANA}/compare_similarity_group.py ${VEC}.csv ${DATA_DIR}/words.csv > mean_dissimilarity.txt
python ${DIR_ANA}/MDSanalysis.py ${VEC}.csv ${DATA_DIR}/words.csv

for N_ELEMENT in 1 2 3 4 5
do
    python ${DIR_EVAL}/eval_mikolovdata_sparse.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt ${VEC}.csv ${DATA_DIR}/words.csv ${N_ELEMENT} > result_mikolovtest_${VEC}_sparse_${N_ELEMENT}.txt
done

