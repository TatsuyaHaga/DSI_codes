#!/bin/bash

DATA=enwiki_processed_pickle
#DATA=wikitext103train_processed_pickle

time python gen_state_seq_words.py $DATA 1000 > gen_state_seq_log.txt
time python count_successor.py state_seq.csv 0.9
