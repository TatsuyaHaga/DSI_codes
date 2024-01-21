#!/bin/bash

python analysis_gridness.py vector_from.csv > gridness_results.txt
python plot_gridcells.py vector_from.csv
mkdir plot_vec_from
mv rep*.svg grid*.svg gridness_results.txt gridness.csv is_gridcell.csv grid_scale.csv plot_vec_from

python analysis_gridness.py vector_goal.csv > gridness_results.txt
python plot_gridcells.py vector_goal.csv
mkdir plot_vec_goal
mv rep*.svg grid*.svg gridness_results.txt gridness.csv is_gridcell.csv grid_scale.csv plot_vec_goal
