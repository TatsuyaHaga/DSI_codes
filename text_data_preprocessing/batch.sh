#!/bin/bash

DIR_INPUT=text
DIR=enwiki_corpus_files

mkdir ${DIR}
python build_corpus_enwiki.py ${DIR_INPUT} ${DIR}/enwiki_data_pickle > ${DIR}/build_corpus_log.txt
python filter_corpus.py ${DIR}/enwiki_data_pickle ${DIR}/enwiki_filtered_pickle 0 > ${DIR}/filtering_log.txt
python pickle2txt.py ${DIR}/enwiki_filtered_pickle ${DIR}/enwiki_filtered_1d.txt

python extract_sentense.py ${DIR}/enwiki_data_pickle 0 > ${DIR}/example.txt
python extract_sentense.py ${DIR}/enwiki_filtered_pickle 0 > ${DIR}/example_filtered.txt
