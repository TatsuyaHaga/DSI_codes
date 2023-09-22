#!/usr/bin/env python

import numpy
import pandas

ws353 = pandas.read_csv("wordsim353/combined.csv")
print(ws353)
print(ws353.loc[:,"Word 1"])

mikolov_test = pandas.read_csv("google_analogy_test_set/questions-words.txt", sep=" ", comment=":", header=None)
print(mikolov_test)
print(mikolov_test.iloc[0,1])
