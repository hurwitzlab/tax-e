#!/bin/bash

D1_SUB_IN="../data/go/d1_subsample"
D1_SUB_OUT="../data/freqs/d1_subsample"
MERGE="./merge_go.py -n log"

$MERGE -o ${D1_SUB_OUT}/all.csv $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/binding.csv -f go_parsing/binding/GO_0005488 $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/catalytic.csv -f go_parsing/catalytic_activity/GO_0003824 $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/metabolic.csv -f go_parsing/metabolic_process/GO_0008152 $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/go_mol_func.csv -f go_parsing/old/MF_CC_BP/GO_0003674 $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/go_cell_comp.csv -f go_parsing/old/MF_CC_BP/GO_0005575 $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/go_bio_proc.csv -f go_parsing/old/MF_CC_BP/GO_0008150 $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/ion_trans.csv -f go_parsing/old/ion_transport/GO_0006811 $D1_SUB_IN
$MERGE -o ${D1_SUB_OUT}/oxidation.csv -f go_parsing/old/oxidation_reduction/subclasses_of_GO_0055114.txt $D1_SUB_IN

for i in $(seq 2 10); do
    n=$(printf "%02d" $i)
    $MERGE -d $i -o ${D1_SUB_OUT}/depth_${n}.csv $D1_SUB_IN
done
