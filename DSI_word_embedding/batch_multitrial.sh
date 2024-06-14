#!/bin/bash

for D1 in decorr decorr_nonnegOFF sparse
do
    for D2 in 1 #2 3 4 5
    do
        DIR=DSI_${D1}_trial${D2}
        cp -r DSI_${D1} ${DIR}
        cd ${DIR}
        pwd
        bash batch.sh
        cd ../
    done
done
