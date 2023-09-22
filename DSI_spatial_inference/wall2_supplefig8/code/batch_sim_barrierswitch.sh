#!/bin/bash

python create_network_barrierswitch_wall2.py
for NUM in 1 2 3 4 5 6 7 8 9 10
do
    python gen_state_seq_barrierswitch.py part$NUM
done
cat state_seqpart*.csv > state_seq.csv
rm state_seqpart*.csv
