#!/bin/bash

for N in 1 2; do
    for NORM in none log tf; do
        IN_DIR="../data/freqs_${N}/${NORM}/"

        if [[ ! -d "$IN_DIR" ]]; then
            echo "Bad IN_DIR \"$IN_DIR\""
            continue
        fi

        OUT_DIR="../figures/d${N}_subsample/${NORM}"

        [[ ! -d "$OUT_DIR" ]] && mkdir -p "$OUT_DIR"

        FILES=$(mktemp)
        find "$IN_DIR" -type f -name \*.csv > "$FILES"

        while read -r FILE; do
            BASENAME=$(basename "$FILE" ".csv")
            TITLE="D${N} $BASENAME $NORM"
            OUT_FILE="$OUT_DIR/$BASENAME.png"
            if [[ ! -f "$OUT_FILE" ]]; then
                echo $TITLE
                ./compare_models.py -q -t "$TITLE" -o "$OUT_FILE" "$FILE" 2>/dev/null
            fi
        done < "$FILES"

        rm "$FILES"
    done
done
echo "Done."

