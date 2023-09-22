#!/bin/bash

DIR_EVAL=../dataset_eval
DIR_ANA=../analysis_codes

python split_vector_data.py vectors.txt
python ${DIR_EVAL}/eval_WS353.py ${DIR_EVAL}/wordsim353/combined.csv vector.csv words.csv > result_WS353.txt
python ${DIR_EVAL}/eval_mikolovdata.py ${DIR_EVAL}/google_analogy_test_set/questions-words.txt vector.csv words.csv > result_mikolovtest.txt
python ${DIR_ANA}/analysis_vector.py vector.csv words.csv > units_${VEC}.txt
python ${DIR_ANA}/analysis_unit_similarity.py vector.csv words.csv > similarity_eachunit_${VEC}.txt

bash batch_mikolov_sparse.sh

