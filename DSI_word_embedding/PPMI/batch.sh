#!/bin/bash

python gen_state_seq_words.py ../enwiki_filtered_pickle 1000
python PPMI.py state_seq.csv 10
python compress_svd.py PPMI.csv 300

DIR_EVAL=../dataset_eval
DIR_ANA=../analysis_codes
VEC=vector_left
python ${DIR_EVAL}/eval_WS353.py ${DIR_EVAL}/wordsim353/combined.csv ${VEC}.csv words.csv > result_WS353_${VEC}.txt
python ${DIR_EVAL}/eval_mikolovdata.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt ${VEC}.csv words.csv > result_mikolovtest_${VEC}.txt
python ${DIR_ANA}/analysis_vector.py ${VEC}.csv words.csv > units_${VEC}.txt
python ${DIR_ANA}/analysis_unit_similarity.py ${VEC}.csv words.csv > similarity_eachunit_${VEC}.txt

bash batch_mikolov_sparse.sh
