import nltk
import sys
import pickle
import itertools
import string

with open(sys.argv[1], "rb") as f:
    data = pickle.load(f)
outfile = sys.argv[2]
min_count = int(sys.argv[3])

Ndata = len(data)
data1d = list(itertools.chain(*data))
Ntoken_before = len(data1d)
Nvocab_before = len(sorted(set(data1d)))

#lower case, removal of punctuation characters
for n in range(Ndata):
    data[n] = [w.lower() for w in data[n] if w not in string.punctuation]
    #data[n] = [w.lower() for w in data[n]]

if min_count>1:
    data1d = list(itertools.chain(*data))
    wordcount = nltk.FreqDist(data1d)
    for n in range(Ndata):
        for idx, w in enumerate(data[n]):
            if wordcount[w]<min_count:
                data[n][idx] = "<unk>"

#save results
with open(outfile, "wb") as f:
    pickle.dump(data, f)

data1d = list(itertools.chain(*data))
Ntoken_after = len(data1d)
Nvocab_after = len(sorted(set(data1d)))

print("min_count=", min_count)
print("lowercase all words.")
print("punctuation characters removed.")
print("number of vocabulary: ", Nvocab_before, "->", Nvocab_after)
print("number of tokens: ", Ntoken_before, "->", Ntoken_after)
