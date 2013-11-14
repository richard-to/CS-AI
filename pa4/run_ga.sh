#!/bin/bash

COUNT=1

for OSEED in 10 21 32 44 433
do
    for SEED in 121 990 343 22 2133
    do
        echo "Starting run $COUNT:"
        echo "Run $COUNT" >> results.txt
        python ga.py -o $OSEED -s $SEED >> results.txt
        echo " " >> results.txt
        (( ++COUNT ))
    done
done