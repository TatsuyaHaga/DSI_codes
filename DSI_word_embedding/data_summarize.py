#!/usr/bin/env python

import numpy
import re
import sys

label = sys.argv[1]#["decorr", "sparse", "decorr_nonnegOFF"]

data = numpy.zeros([5, 9])
for n in range(5):
    with open("DSI_"+label+"_trial"+str(n+1)+"/similarity_eachunit_vector_from.txt", "r") as f:
        text = f.read()#.splitlines()[-1]
        d = re.search(r"ratio of significant units=.*,", text).group()
        d = float(d.lstrip("ratio of significant units=").rstrip(","))
        data[n, 0] = d
        d = re.search(r"concept specificity\nAll units: mean=.*,", text).group()
        d = float(d.lstrip("concept specificity\nAll units: mean=").rstrip(","))
        data[n, 1] = d

    with open("DSI_"+label+"_trial"+str(n+1)+"/result_WS353_vector_from.txt", "r") as f:
        text = f.read()#.splitlines()[-1]
        d = re.search(r"WS353 = .*,", text).group()
        d = float(d.lstrip("WS353 = ").rstrip(","))
        data[n, 2] = d

    for i in range(5):
        with open("DSI_"+label+"_trial"+str(n+1)+"/result_mikolovtest_vector_from_sparse_"+str(i+1)+".txt", "r") as f:
            text = f.read()#.splitlines()[-1]
            d = re.search(r"correct rate = .*\(", text).group()
            d = float(d.lstrip("correct rate = ").rstrip("\()"))
            data[n, 3+i] = d

    with open("DSI_"+label+"_trial"+str(n+1)+"/result_mikolovtest_vector_from.txt", "r") as f:
        text = f.read()#.splitlines()[-1]
        d = re.search(r"correct rate = .*\(", text).group()
        d = float(d.lstrip("correct rate = ").rstrip("\()"))
        data[n, 8] = d

numpy.savetxt("DSI_"+label+".csv", data, delimiter=",")