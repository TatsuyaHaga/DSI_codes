import nltk
nltk.download("punkt")
import sys
import os
import random
import pickle
import itertools

#paths of text files
rootdir=sys.argv[1] #directory of extracted text files
paths=[]
for curdir, dirs, files in os.walk(rootdir):
    for fname in files:
        paths.append(curdir+"/"+fname)
random.shuffle(paths) #to randomly select articles

outfile = sys.argv[2] #output file name

#parameters
min_words_line = 0
min_words_page = 1000
max_readnum = 100000 #If negative, all articles are imported.

print("min_words_line=", min_words_line, ", min_words_page=", min_words_page, "max_readnum=", max_readnum)

#import
data = []
readnum = 0
reject_num = 0
token_num = 0
for nf, path in enumerate(paths):
    print("opening", path, nf+1, "/", len(paths), flush=True)
    with open(path) as fp:
        article = []
        title_skip = False
        for line in fp:
            if line[:5]=="<doc ": #beginning of a document
                title_skip = True
                continue
            if title_skip: #skip title
                title_skip = False
                continue
            if line=="\n": #empty line, end of a paragraph
                continue 
            if line[:6]=="</doc>": #end of a document
                if len(article)>min_words_page:
                    data.append(article)
                    readnum+=1
                else:
                    reject_num+=1
                article = []
                if max_readnum<0 or readnum<max_readnum:
                    continue
                else:
                    break
            #import tokens
            tokens = nltk.tokenize.word_tokenize(line)
            if len(tokens)>=min_words_line: # add paragraph or not
                article.extend(tokens)
                token_num += len(tokens)
    print(readnum, "articles imported. ", reject_num, "articles rejected.", token_num, "tokens.", flush=True)
    if max_readnum>=0 and readnum>=max_readnum:
        break

with open(outfile, "wb") as f:
    pickle.dump(data, f)

print("Process end. Data contain", readnum, "articles,", token_num, "tokens.")
