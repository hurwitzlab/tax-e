#!/bin/bash

#
# This script will select features for datasets 1 and 2 using normalizations
# of "tf" (term-frequence) and "log".
#
# Authors: Kai Blumberg, Ken Youens-Clark
#

for N in 1 2; do
    GO_DIR="../data/go/d${N}_subsample"

    echo "Processing GO_DIR \"$GO_DIR\""

    for NORM in log tf; do
        MERGE="./merge_go.py -n $NORM"
        OUT_DIR="../data/freqs_${N}/$NORM"

        [[ ! -d "$OUT_DIR" ]] && mkdir -p "$OUT_DIR"

        if [[ ! -d "$GO_DIR" ]]; then
            echo "Bad GO_DIR \"$GO_DIR\""
            exit 1
        fi

        # 
        # No feature selection
        #
        $MERGE -o ${OUT_DIR}/all.csv $GO_DIR

        #
        # Using GO hierarchy to trim further into tree
        #
        for i in $(seq 2 10); do
            n=$(printf "%02d" $i)
            $MERGE -d $i -o ${OUT_DIR}/depth_${n}.csv $GO_DIR
        done

        #
        # Nucleoside-triphosphatase activity
        #
        $MERGE -o ${OUT_DIR}/nucleoside-triphosphatase_activity.csv -f go_parsing/nucleoside-triphosphatase_activity/GO_0017111 $GO_DIR

        #
        # Translation-associated features
        #
        $MERGE -o ${OUT_DIR}/translation_assoc.csv -f go_parsing/translation_assoc/translation_assoc.txt $GO_DIR

        #
        # Super-classes from 10-level trimming
        #
        $MERGE -o ${OUT_DIR}/alpha-amino_acid_biosynthetic_process.csv -f go_parsing/alpha-amino_acid_biosynthetic_process/subclasses_of_GO_1901607.txt $GO_DIR
        $MERGE -o ${OUT_DIR}/ATPase_activity.csv -f go_parsing/ATPase_activity/subclasses_of_GO_0016887.txt $GO_DIR
        $MERGE -o ${OUT_DIR}/ATP_biosynthetic_process.csv -f go_parsing/ATP_biosynthetic_process/subclasses_of_GO_0006754.txt $GO_DIR
        $MERGE -o ${OUT_DIR}/nucleoside_phosphate_metabolic_process.csv -f go_parsing/nucleoside_phosphate_metabolic_process/GO_0006753 $GO_DIR
        $MERGE -o ${OUT_DIR}/tRNA_metabolic_process.csv -f go_parsing/tRNA_metabolic_process/subclasses_of_GO_0006399.txt $GO_DIR
    done
done

echo "Done."
