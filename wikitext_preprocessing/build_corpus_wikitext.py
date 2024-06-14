import nltk
nltk.download("punkt")
import sys
import pickle

#paths of text files
fname=sys.argv[1] #directory of extracted text files
outfile = sys.argv[2] #output file name

#import
data = []
article = []
readnum = 0
token_num = 0
print("opening", fname)
fp = open(fname)
for line in fp:
    if line=="\n" or line==" \n": #empty line, skipped
        continue
    elif line[:3]==" = ": #beginning of a document
        if len(article)>0:
            data.append(article)
            readnum+=1
            article = []
            if readnum%10000==0:
                print(f"{readnum} articles read.")
    else:
        #import tokens
        line = line.replace("<unk>", "unk") # to avoid decomposition of <unk> tokens.
        tokens = nltk.tokenize.word_tokenize(line)
        tokens = ["<unk>" if x=="unk" else x for x in tokens]
        article.extend(tokens)
        token_num += len(tokens)

#after end of data
if len(article)>0:
    data.append(article)
    readnum+=1
    article = []

with open(outfile, "wb") as f:
    pickle.dump(data, f)

print("Process end. Data contain", readnum, "articles,", token_num, "tokens.")
