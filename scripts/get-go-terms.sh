#!/bin/bash

#
# For each CSV file in the "metagenomes" dir, get the associated GO terms
# Author: Ken Youens-Clark <kyclark@email.arizona.edu>
#

set -u

METAGENOMES_DIR="../metagenomes/all"
GO_DIR="../data/go"
MAX=100

if [[ ! -d "$METAGENOMES_DIR" ]]; then
    echo "Missing expected METAGENOMES_DIR \"$METAGENOMES_DIR\""
    exit 1
fi

METAGENOMES=$(mktemp)
find "$METAGENOMES_DIR" -type f > "$METAGENOMES"

while read -r FILE; do
    METAGENOME=$(basename "$FILE" ".csv")
    echo "Extracting accessions from \"$METAGENOME\""

    OUT_DIR="$GO_DIR/$METAGENOME"

    [[ ! -d "$OUT_DIR" ]] && mkdir -p "$OUT_DIR"

    ACCS=$(mktemp)
    awk -F',' 'NR>1 {print $1 "\t" $7}' "$FILE" | sed 's/"//g'  > "$ACCS"

    i=0
    while read -r ACC ERR; do
        i=$((i+1))
        #URL="https://www.ebi.ac.uk/metagenomics/api/v1/analyses/${ACC}/file/${ERR}_FASTA_InterPro.tsv.gz"
        URL="https://www.ebi.ac.uk/metagenomics/api/v1/analyses/${ACC}/file/${ERR}_MERGED_FASTQ_GO.csv"
        FILE=$(basename "$URL")
        printf "%3d: %s\n" $i "$URL"
        (cd "$OUT_DIR" && wget --no-clobber "$URL")
        if [[ $i -gt $MAX ]]; then
            break
        fi
    done < "$ACCS"
done < "$METAGENOMES"

echo "Done."
