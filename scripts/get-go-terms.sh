#!/bin/bash

#
# For each CSV file in the "metagenomes" dir, get the associated GO terms
# Author: Ken Youens-Clark <kyclark@email.arizona.edu>
# Modifications: Kai Blumberg <kblumberg@email.arizona.edu>
#

set -u

# Get go data from the from the subsampled low resolution taxonomic data, dataset 1
METAGENOMES_DIR_1="../metagenomes/dataset_2_subsample"
GO_DIR_1="../data/go/d2_subsample"
MAX=100

if [[ ! -d "$METAGENOMES_DIR_1" ]]; then
    echo "Missing expected METAGENOMES_DIR_1 \"$METAGENOMES_DIR_1\""
    exit 1
fi

METAGENOMES_1=$(mktemp)
find "$METAGENOMES_DIR_1" -type f > "$METAGENOMES_1"

while read -r FILE; do
    METAGENOME=$(basename "$FILE" ".csv")
    echo "Extracting accessions from \"$METAGENOME\""

    OUT_DIR="$GO_DIR_1/$METAGENOME"

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
        if [[ $i -eq $MAX ]]; then
            break
        fi
    done < "$ACCS"
done < "$METAGENOMES_1"

# Get go data from the from the subsampled low resolution taxonomic data, dataset 1
# Note we are using verison 2.0 of the EBI_pipeline for this dataset

# METAGENOMES_DIR_2="../metagenomes/dataset_2_subsample"
# GO_DIR_2="../data/go_2"
# MAX=100
#
# if [[ ! -d "$METAGENOMES_DIR_2" ]]; then
#     echo "Missing expected METAGENOMES_DIR_2 \"$METAGENOMES_DIR_2\""
#     exit 1
# fi
#
# METAGENOMES_2=$(mktemp)
# find "$METAGENOMES_DIR_2" -type f > "$METAGENOMES_2"
#
# while read -r FILE; do
#     METAGENOME=$(basename "$FILE" ".csv")
#     echo "Extracting accessions from \"$METAGENOME\""
#
#     OUT_DIR="$GO_DIR_2/$METAGENOME"
#
#     [[ ! -d "$OUT_DIR" ]] && mkdir -p "$OUT_DIR"
#
#     ACCS=$(mktemp)
#     awk -F',' 'NR>1 {print $1 "\t" $7}' "$FILE" | sed 's/"//g'  > "$ACCS"
#
#     i=0
#     while read -r ACC ERR; do
#         i=$((i+1))
#         #URL="https://www.ebi.ac.uk/metagenomics/api/v1/analyses/${ACC}/file/${ERR}_FASTA_InterPro.tsv.gz"
#         URL="https://www.ebi.ac.uk/metagenomics/api/v1/analyses/${ACC}/file/${ERR}_MERGED_FASTQ_GO.csv"
#         FILE=$(basename "$URL")
#         printf "%3d: %s\n" $i "$URL"
#         (cd "$OUT_DIR" && wget --no-clobber "$URL")
#         if [[ $i -eq $MAX ]]; then
#             break
#         fi
#     done < "$ACCS"
# done < "$METAGENOMES_2"

echo "Done."
