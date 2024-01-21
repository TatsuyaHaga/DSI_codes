#!/bin/bash

#execute first -> wait until finishing all calcualation
#bash batch_sim_barrierswitch.sh

bash batch_sim_barrierswitch_concat.sh
bash batch_learn.sh
bash batch_plot_infer.sh
bash batch_analysis_gridness.sh

bash batch_navigation_combi.sh
bash batch_navigation_combi_sparse_AB.sh
bash batch_navigation_combi_sparse_AB_grid.sh
