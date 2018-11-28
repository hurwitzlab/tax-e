#!/bin/bash

D1_SUB_IN="../data/go/d1_subsample"
D1_SUB_OUT="../data/freqs_1/log"
MERGE="./merge_go.py -n log"

# nucleoside-triphosphatase activity
#$MERGE -o ${D1_SUB_OUT}/nucleoside-triphosphatase_activity.csv -f go_parsing/nucleoside-triphosphatase_activity/GO_0017111 -i $D1_SUB_IN

#Translation associated features
$MERGE -o ${D1_SUB_OUT}/translation_assoc.csv -f go_parsing/translation_assoc/translation_assoc.txt -i $D1_SUB_IN


$MERGE -o ${D1_SUB_OUT}/alpha-amino_acid_biosynthetic_process.csv -f go_parsing/alpha-amino_acid_biosynthetic_process/subclasses_of_GO_1901607.txt -i $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/ATPase_activity.csv -f go_parsing/ATPase_activity/subclasses_of_GO_0016887.txt -i $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/ATP_biosynthetic_process.csv -f go_parsing/ATP_biosynthetic_process/subclasses_of_GO_0006754.txt -i $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/nucleoside_phosphate_metabolic_process.csv -f go_parsing/nucleoside_phosphate_metabolic_process/GO_0006753 -i $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/tRNA_metabolic_process.csv -f go_parsing/tRNA_metabolic_process/subclasses_of_GO_0006399.txt -i $D1_SUB_IN

$MERGE -o ${D1_SUB_OUT}/all.csv -i $D1_SUB_IN

for i in $(seq 2 10); do
    n=$(printf "%02d" $i)
    $MERGE -d $i -o ${D1_SUB_OUT}/depth_${n}.csv -i $D1_SUB_IN
done

D1_SUB_IN="../data/go/d1_subsample"
D1_SUB_OUT="../data/freqs_1/tf"
MERGE="./merge_go.py -n tf"

$MERGE -o ${D1_SUB_OUT}/all.csv -i $D1_SUB_IN

for i in $(seq 2 10); do
    n=$(printf "%02d" $i)
    $MERGE -d $i -o ${D1_SUB_OUT}/depth_${n}.csv -i $D1_SUB_IN
done

D1_SUB_IN="../data/go/d1_subsample"
D1_SUB_OUT="../data/freqs_1/nlog_tf"
MERGE="./merge_go.py -n nlog_tf"

$MERGE -o ${D1_SUB_OUT}/all.csv -i $D1_SUB_IN

for i in $(seq 2 10); do
    n=$(printf "%02d" $i)
    $MERGE -d $i -o ${D1_SUB_OUT}/depth_${n}.csv -i $D1_SUB_IN
done

D1_SUB_IN="../data/go/d1_subsample"
D1_SUB_OUT="../data/freqs_1/aug_freq"
MERGE="./merge_go.py -n aug_freq"

$MERGE -o ${D1_SUB_OUT}/all.csv -i $D1_SUB_IN

for i in $(seq 2 10); do
    n=$(printf "%02d" $i)
    $MERGE -d $i -o ${D1_SUB_OUT}/depth_${n}.csv -i $D1_SUB_IN
done
