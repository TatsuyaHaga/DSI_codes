# DSI\_codes
Codes for Tatsuya Haga, Yohei Oseki, Tomoki Fukai, "A unified neural representation model for spatial and semantic computations"

## Dependency
We used a UNIX environment (ubuntu 20.04), a GPU (NVIDIA GeForce RTX 3090) with CUDA 12.1, Python 3.10, and following Python libraries:
numpy 1.23, scipy 1.10, nltk 3.7, gensim 4.3, networkx 2.8, cupy 12.0, matplotlib 3.6, pygraphviz 1.9, pandas 1.5, scikit-learn 1.2.

An environment of Anaconda/Miniconda is given by a file `env_DSI.yml`.

`conda env create -f env_DSI.yml`

`conda activate DSI`

We note that parallel processing of 12 - 16 threads runs in the codes.

## DSI\_2Dspace, DSI\_maze
Codes for Figure 2 and 3, and Figure S15. Execute `bash batch_all.sh` in each directory, or manually execute individual commands in shell scripts. Outputs are figures and txt files in which quantitative values are written. Run time was several minutes.

## DSI\_spatial\_inference
Codes for Figure 7. To obtain results, execute `batch_multitrial.sh`. Five simulations are repeated and summarized by batch_multitrial.sh. Run time was about 1 hour per simulation. 


## DSI\_word\_embedding
Main codes for Figure 4, 5, and 6. 

1. Download WS353 dataset at http://alfonseca.org/eng/research/wordsim353.html and Mikolov's dataset at https://aclweb.org/aclwiki/Google_analogy_test_set_(State_of_the_art) . Put them in `dataset_eval` directory.

2. Download preprocessed text data at Zenodo (https://doi.org/10.5281/zenodo.11651117).  Put the data in `text_data` directory, and execute `bash batch_count.sh` to calculate word counts and SR. enwiki_processed_pickle is a main dataset based on English Wikipedia dump taken on 22-May-2020 (https://dumps.wikimedia.org/enwiki/latest/). wikitext103train_processed_pickle is an additional dataset based on WikiText-103 dataset (Stephen Merity, Caiming Xiong, James Bradbury, and Richard Socher. 2016. Pointer Sentinel Mixture Models. http://arxiv.org/abs/1609.07843).

3. Execute `bash batch.sh` in each directory. Outputs are figures and txt files in which TOP-10 words for each unit and quantitative values are output. Run time was approximately 1 hour for each condition. `batch_multitrial.sh` automatically repeats 5 trials for each condition of DSI learning (with different random seeds).

4. Codes for GLoVe were not included. Apply the code `pickle2txt.py` in text\_data\_preprocessing directory to pickle files in Zenodo. Then, apply codes at https://github.com/stanfordnlp/GLoVe to the generated text file and put an output file `vectors.txt` in the directory `glove_eval`.Then execute `bash batch.sh` in `glove_eval`. 

5. `result_summary` is for plotting a summary of all methods. We put data that we plotted in the article. `data_summarize.py` helps summarizing results after `batch_multitrial.sh`.

## text\_data\_preprocessing
Preprocessing codes used for Wikipedia dump. (not necessary if you use preprocessed files in Zenodo)

1. Download a wikipedia dump file enwiki-latest-pages-articles.xml.bz2 at https://dumps.wikimedia.org/enwiki/latest/ .

2. Apply Wikiextractor ( https://github.com/attardi/wikiextractor ) to the dump file. Put the output directory `text` in text_data_preprocessing and execute `bash batch.sh`.

## wikitext\_preprocessing
Preprocessing codes used for WikiText-103 dataset (https://dagshub.com/DagsHub/WIkiText-103). (not necessary if you use preprocessed files in Zenodo) 

Put wiki.train.tokens (training data) of WikiText-103 in the directory and execute `bash batch.sh`.