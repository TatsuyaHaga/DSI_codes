#!/bin/bash

bash batch_sim2Dspace.sh
bash batch_learn.sh

bash batch_navigation.sh
mkdir decisionmaking_results
mv decision_making*.svg decisionmaking_result.txt decisionmaking_results/
