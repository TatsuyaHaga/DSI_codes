#!/bin/bash

python plot_analysis_grid.py vector_from.csv > gridness_results.txt
mkdir plot_vec_from
mv rep*.svg grid*.svg gridness_results.txt plot_vec_from

python plot_analysis_grid.py vector_goal.csv > gridness_results.txt
mkdir plot_vec_goal
mv rep*.svg grid*.svg gridness_results.txt plot_vec_goal
