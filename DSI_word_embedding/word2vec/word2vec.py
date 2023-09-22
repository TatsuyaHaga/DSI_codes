import gensim
import nltk
import sys
import pickle
import itertools
import random
import numpy

if sys.argv[1]=="skipgram":
    sg_flag = 1
elif sys.argv[1]=="cbow":
    sg_flag = 0
else:
    print("Please specify skipgram or cbow.")

with open(sys.argv[2], "rb") as f:
    data=pickle.load(f)
vec_size = int(sys.argv[3]) #dimension of vectors
win_size = int(sys.argv[4])
min_count = int(sys.argv[5])
ns_exponent = 0.75
print("data including", len(list(itertools.chain(*data))), "tokens,", f"create {vec_size}-D vectors, win_size={win_size}, min_count={min_count}")

model=gensim.models.Word2Vec(data, sg=sg_flag, hs=0, vector_size=vec_size, min_count=min_count, window=win_size, ns_exponent=ns_exponent, workers=16)
model.save("learned_model")
list_words=model.wv.index_to_key
Nw = len(list_words)
print("vectorized", Nw, "words")

vectors = numpy.zeros([Nw, vec_size])
for i in range(Nw):
    vectors[i,:] = model.wv.get_vector(list_words[i])

with open("words.csv", "w") as f:
    for x in list_words:
        f.write(x+"\n")
numpy.savetxt("vector.csv", vectors, delimiter=",")
