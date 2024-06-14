#/bin/bash

python build_corpus_wikitext.py wiki.train.tokens wikitext103train_pickle > build_corpus_log.txt
python filter_corpus.py wikitext103train_pickle wikitext103train_processed_pickle 0 > filter_log.txt
