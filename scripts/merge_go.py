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
def main():
    """main"""
    args = get_args()
    in_dir = args.indir
    out_file = args.outfile

    if not os.path.isdir(in_dir):
        die('--indir "{}" is not a directory'.format(indir))

    matrix = pd.DataFrame({'term': []})
    for i, file in enumerate(os.listdir(in_dir)):
        fpath = os.path.join(in_dir, file)
        if not os.path.isfile(fpath):
            continue

        # ERR2281809_MERGED_FASTQ_GO.csv => ERR2281809
        run_name = file.split('_')[0]
        col_names = ['term', 'desc', 'domain', run_name]
        drop_cols = ['desc', 'domain']
        print("{:3}: {}".format(i + 1, run_name))

        df = pd.read_csv(fpath, names=col_names).drop(drop_cols, axis=1)
        matrix = pd.merge(matrix, df, on='term', how='outer').fillna(0)

    matrix.set_index('term', inplace=True)
    matrix.to_csv(out_file, sep=',', encoding='utf-8')

    print('Done')


# --------------------------------------------------
if __name__ == '__main__':
    main()
