#!/bin/bash

bash batch_sim_barrierswitch.sh
bash batch_learn.sh
bash batch_plot_infer.sh
bash batch_analysis_contextchange.sh

bash batch_navigation_combi.sh
bash batch_navigation_combi_sparse_AB.sh
bash batch_navigation_combi_sparse_AB_grid.sh
