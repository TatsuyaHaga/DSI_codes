#!/bin/bash

DIR_EVAL=../dataset_eval
DIR_ANA=../analysis_codes

VEC=vector
for MODE in skipgram cbow
do
    time python word2vec.py ${MODE} ../enwiki_filtered_pickle 300 10 1000
    
    python ${DIR_EVAL}/eval_WS353.py ${DIR_EVAL}/wordsim353/combined.csv vector.csv words.csv > result_WS353.txt
    python ${DIR_EVAL}/eval_mikolovdata.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt vector.csv words.csv > result_mikolovtest.txt
    python ${DIR_ANA}/analysis_vector.py ${VEC}.csv words.csv > units_${VEC}.txt
    python ${DIR_ANA}/analysis_unit_similarity.py ${VEC}.csv words.csv > similarity_eachunit_${VEC}.txt
    bash batch_mikolov_sparse.sh

    mkdir ${MODE}_result
    mv *.csv *.txt learned_model ${MODE}_result
done

