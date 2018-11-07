#!/bin/bash

#
# Run "merge_go.py" for each of the frequency matrices by metagenome
# Author: Ken Youens-Clark <kyclark@email.arizona.edu>
#

IN_DIR="../data/go"
OUT_DIR="../data/freqs"

for DIR in $IN_DIR/*; do
    echo $DIR
    ./merge_go.py -n -i "$DIR" -o "$OUT_DIR/$(basename "$DIR").csv"
done

echo "Done."
