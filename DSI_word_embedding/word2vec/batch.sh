#!/bin/bash

DATA_FILE=../text_data/enwiki_processed_pickle
#DATA_FILE=../text_data/wikitext103train_processed_pickle
DIR_EVAL=../dataset_eval
DIR_ANA=../analysis_codes

VEC=vector
for MODE in skipgram cbow
do
    time python word2vec.py ${MODE} ${DATA_FILE} 300 10 1000
    
    python ${DIR_EVAL}/eval_WS353.py ${DIR_EVAL}/wordsim353/combined.csv ${VEC}.csv words.csv > result_WS353.txt
    python ${DIR_EVAL}/eval_mikolovdata.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt ${VEC}.csv words.csv > result_mikolovtest.txt
    python ${DIR_ANA}/analysis_vector.py ${VEC}.csv words.csv > units_${VEC}.txt
    python ${DIR_ANA}/analysis_unit_similarity.py ${VEC}.csv words.csv > similarity_eachunit_${VEC}.txt

    for N_ELEMENT in 1 2 3 4 5
    do
        python ${DIR_EVAL}/eval_mikolovdata_sparse.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt ${VEC}.csv words.csv ${N_ELEMENT} > result_mikolovtest_${VEC}_sparse_${N_ELEMENT}.txt
    done

    mkdir ${MODE}_result
    mv *.csv *.txt learned_model ${MODE}_result
done

