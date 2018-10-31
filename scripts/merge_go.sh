#!/bin/bash

for DIR in go/*; do
    echo $DIR
    ./merge_go.py -i "$DIR" -o freqs/$(basename "$DIR").csv
done
