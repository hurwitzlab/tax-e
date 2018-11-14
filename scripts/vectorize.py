#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-10-29
Purpose: Merge GO terms for each metagenome into a frequency matrix
"""

import argparse
import csv
import os
import sys
import pandas as pd
from collections import defaultdict
from sklearn.feature_extraction import DictVectorizer


# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='Merge GO terms into a frequence matrix',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-i',
        '--indir',
        help='Directory with GO counts for each sample',
        metavar='str',
        type=str,
        default='go')

    parser.add_argument(
        '-o',
        '--outfile',
        help='Output matrix file',
        metavar='str',
        type=str,
        default='go-freq.csv')

    parser.add_argument(
        '-n',
        '--normalize',
        help='Normalize frequency by count of terms',
        action='store_true')

    return parser.parse_args()


# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
def find_dirs(in_dir):
    if not os.path.isdir(in_dir):
        die('--indir "{}" is not a directory'.format(indir))

    dirs = []
    for path in os.scandir(in_dir):
        if path.is_dir():
            dirs.append(path)

    if not dirs:
        die('Found no subdirectories in "{}"'.format(in_dir))

    return dirs


# --------------------------------------------------
def main():
    """main"""
    args = get_args()
    in_dir = args.indir
    out_file = args.outfile

    #matrix.set_index('term')

    biome_dfs = []
    i = 0

    for biome_dir in find_dirs(args.indir):
        biome_name = biome_dir.name
        #biome_df = pd.DataFrame({'term': []})
        biome_data = []

        for file in os.scandir(biome_dir):
            if not file.is_file():
                continue

            matrix = defaultdict(int)
            with open(file.path) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    go, count = row[0], row[-1]
                    matrix[go] = count
            print(matrix)
            biome_data.append(matrix)

        v = DictVectorizer(sparse=False)
        X = v.fit_transform(biome_data)
        print(X)
        print(X.get_feature_names())

def read_file(file):
    #run_name = file.name.split('_')[0]
    run_name = os.path.basename(file).split('_')[0]
    col_names = ['term', 'desc', 'domain', run_name]
    drop_cols = ['desc', 'domain']

    df = pd.read_csv(#file.path
        file, names=col_names).drop(drop_cols, axis=1)

    return df

# --------------------------------------------------
if __name__ == '__main__':
    main()
