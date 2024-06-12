#!/bin/bash

for DIR in trial1 trial2 trial3 trial4 trial5
do
    cp -r code $DIR
    cd $DIR
    pwd
    bash batch_all.sh
    cd ../
done

python result_summary_all.py
