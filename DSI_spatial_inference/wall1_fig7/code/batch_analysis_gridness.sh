#!/bin/bash

python inference_vectors.py B vector_from.csv vector_from_B.csv
python inference_vectors.py C vector_from.csv vector_from_C.csv
python analysis_gridness.py vector_from_C.csv > gridness_results_C.txt

python analysis_rep_distance.py vector_from_B.csv vector_from_C.csv is_gridcell.csv gridness.csv

