#!/usr/bin/env python3
"""
Author : Kai Blumberg
Date   : 2018-11-03
Purpose: subsample from lists of EBI accession biomes.csv files
"""

import argparse
import csv
import os
import sys
import pandas
import random

# #list of panda dataframes to write out.
# df_list = []

# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='subsample  a given number of records from lists of EBI accession biomes.csv files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-i',
        '--indir',
        help='Directory with original EBI biome csv files',
        metavar='str',
        type=str,
        default='../metagenomes/dataset_1')

    parser.add_argument(
        '-o',
        '--outdir',
        help='New subsampled EBI biomes directory',
        metavar='str',
        type=str,
        default='../metagenomes/dataset_1_subsample')

    parser.add_argument(
        '-n',
        '--numMax',
        help='New subsampled EBI biomes directory',
        metavar='int',
        type=int,
        default=38)


    return parser.parse_args()


# --------------------------------------------------
def main():
    """main"""
    args = get_args()
    in_dir = args.indir
    out_dir = args.outdir
    num_Max = args.numMax

    if not os.path.isdir(in_dir):
        die('--indir "{}" is not a directory'.format(indir))

    # write out new randomly subsampled csv files from each of the original .csv files
    for i, file in enumerate(os.listdir(in_dir)):
        fpath = os.path.join(in_dir, file)
        if not os.path.isfile(fpath):
            continue

        n = sum(1 for line in open(fpath)) - 1 #number of records in file (excludes header)
        s = num_Max #desired sample size

        if n <= s:
            df = pandas.read_csv(fpath)
        else:
            skip = sorted(random.sample(range(1,n+1),n-s)) #the 0-indexed header will not be included in the skip list
            df = pandas.read_csv(fpath,  skiprows=skip)

        outpath = os.path.join(out_dir, file)
        #print(outpath)

        df.to_csv(outpath, sep=',', encoding='utf-8',index=False)

# --------------------------------------------------
if __name__ == '__main__':
    main()
