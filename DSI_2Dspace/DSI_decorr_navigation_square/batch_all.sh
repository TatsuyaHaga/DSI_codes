#!/bin/bash

bash batch_sim2Dspace.sh
bash batch_learn.sh
bash batch_plot.sh

bash batch_path_integration.sh
mkdir path_integration_results
mv path_integration*.svg pathintegration_test_random_result.txt path_integration_results/

bash batch_navigation.sh
mkdir decisionmaking_results
mv decision_making*.svg decisionmaking_result.txt decisionmaking_results/
