# DSI\_codes
Codes for Tatsuya Haga, Yohei Oseki, Tomoki Fukai, "A unified neural representation model for spatial and semantic computations"

## Dependency
We used a UNIX environment (ubuntu 20.04), a GPU (NVIDIA GeForce RTX 3090) with CUDA 12.1, Python 3.10, and following Python libraries:
numpy 1.23, scipy 1.10, nltk 3.7, gensim 4.3, networkx 2.8, cupy 12.0, matplotlib 3.6, pygraphviz 1.9, pandas 1.5, scikit-learn 1.2.

An environment of Anaconda/Miniconda is given by a file `env_DSI.yml`.

`conda env create -f env_DSI.yml`

`conda activate DSI`

We note that parallel processing of 12 - 16 threads runs in the codes.

## DSI\_2Dspace
Codes for Figure 2 and 3. Execute `bash batch_all.sh` in each directory, or manually execute individual commands in shell scripts. Outputs are figures and txt files in which quantitative values are written. Run time was several minutes.

## DSI\_spatial\_inference
Codes for Figure 7. In a directory `code`, execute `bash batch_sim_barrierswitch.sh` which initiates several background simulation processes. After all processes finish, execute `bash batch_all.sh`. Run time was about 1 hour per simulation. To obtain statistical results, execute `copy_multitrial.sh` and then repeat five simulations in five copied directories. After finishing simulations, `python result_summary_all.py` generates summarized reults.

## text\_data\_preprocessing
Preprocessing codes for Figure 4, 5, and 6.

1. Download a wikipedia dump file enwiki-latest-pages-articles.xml.bz2 at https://dumps.wikimedia.org/enwiki/latest/ . The version we used (22-May-2020) is available upon request.

2. Apply Wikiextractor ( https://github.com/attardi/wikiextractor ) to the dump file. Put the output directory `text` in text_data_preprocessing and execute `bash batch.sh`.

3. Move output files in `enwiki_corpus_files` to DSI_word_embedding directory.

## DSI\_word\_embedding
Main codes for Figure 4, 5, and 6. 

1. Download WS353 dataset at http://alfonseca.org/eng/research/wordsim353.html and Mikolov's dataset at https://aclweb.org/aclwiki/Google_analogy_test_set_(State_of_the_art) . Put them in `dataset_eval` directory.

2. Execute `bash batch.sh` in each directory. Outputs are figures and txt files in which TOP-10 words for each unit and quantitative values are written. Run time was approximately 1 hour for each condition. 

3. Codes for GLoVe were not included. Apply codes at https://github.com/stanfordnlp/GLoVe to `enwiki_filtered_1d.txt`, and put an output file `vectors.txt` in the directory `glove_eval`.Then execute `bash batch.sh` in `glove_eval`. 

4. `result_summary` is for plotting a summary of all methods. We put data that we plotted in the article.
