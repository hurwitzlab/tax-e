#!/bin/bash

#
# Run "subsample_csv_data.py" for each of the biome.csv files downloaded form EBI_MGnify
# Author: Kai Blumberg <kblumberg@email.arizona.edu>
#

# subsample at most 50 csv rows from the low resolution taxonomic data
#./subsample_csv_data.py -i ../metagenomes/dataset_1/ -o ../metagenomes/dataset_1_subsample -n 50

# subsample at most 38 csv rows from the high resolution taxonomic data
#./subsample_csv_data.py -i ../metagenomes/dataset_2/ -o ../metagenomes/dataset_2_subsample -n 38

# try with only 16 to get rid of duplicates. 
./subsample_csv_data.py -i ../metagenomes/dataset_2/ -o ../metagenomes/dataset_2_subsample -n 38
