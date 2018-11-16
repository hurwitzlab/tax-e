#!/bin/bash

IN_DIR="../data/freqs/d1_subsample/"
OUT_DIR="./figures/d1_subsample"

FILES=$(mktemp)
find "$IN_DIR" -type f -name \*.csv > "$FILES"

[[ ! -d "$OUT_DIR" ]] && mkdir -p "$OUT_DIR"

while read -r FILE; do
    BASENAME=$(basename "$FILE" ".csv")
    echo $BASENAME
    ./compare_models.py -q -T $BASENAME -o $OUT_DIR/$BASENAME.png $FILE
done < "$FILES"

echo "Done."
