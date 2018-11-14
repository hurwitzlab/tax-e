#!/bin/bash

#
# Run "merge_go.py" for each of the frequency matrices by metagenome
# Author: Ken Youens-Clark <kyclark@email.arizona.edu>
# Modifications by Kai Blumberg
#

IN_DIR="../data/go_1"
OUT_DIR="../data/freqs_1"

for DIR in $IN_DIR/*; do
    echo $DIR
    ./merge_go.py -i "$DIR" -o "$OUT_DIR/$(basename "$DIR").csv"
done

IN_DIR="../data/go_2"
OUT_DIR="../data/freqs_2"

for DIR in $IN_DIR/*; do
    echo $DIR
    ./merge_go.py -i "$DIR" -o "$OUT_DIR/$(basename "$DIR").csv"
done


echo "Done."
