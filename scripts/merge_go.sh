#!/bin/bash

#
# Run "merge_go.py" for each of the frequency matrices by metagenome
# Author: Ken Youens-Clark <kyclark@email.arizona.edu>
#

for DIR in go/*; do
    echo $DIR
    ./merge_go.py -i "$DIR" -o freqs/$(basename "$DIR").csv
done

echo "Done."
