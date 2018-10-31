#!/bin/bash

METAGENOMES_DIR="metagenomes"
GO_DIR="go"

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
        if [[ $i -gt 100 ]]; then
            break
        fi
    done < "$ACCS"
done < "$METAGENOMES"

echo "Done."
