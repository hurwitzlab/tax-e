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
import pandas as pd
import random

# #list of panda dataframes to write out.
# df_list = []


# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description=
        'subsample  a given number of records from lists of EBI accession biomes.csv files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-d',
        '--dir',
        help='Directory with original EBI biome csv files',
        metavar='DIR',
        type=str,
        default=None)

    parser.add_argument(
        '-f',
        '--file',
        help='Ordered list of metagenome csv files',
        nargs='+',
        metavar='FILE',
        type=str,
        default=None)

    parser.add_argument(
        '-o',
        '--outdir',
        help='New subsampled EBI biomes directory',
        metavar='str',
        type=str,
        default='../metagenomes/dataset_1_subsample')

    parser.add_argument(
        '-m',
        '--max',
        help='Maximum number of samples per biome/csv',
        metavar='int',
        type=int,
        default=38)

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
    out_dir = args.outdir
    num_max = args.max

    file_list = []
    if args.dir:
        file_list = list(map(lambda p: p.path, os.scandir(args.dir)))
    elif args.file:
        file_list = args.file
    else:
        die('Must have --dir or --file')

    if not file_list:
        die('Found no files?')

    num_files = len(file_list)
    print('Will process {} file{}'.format(num_files,
                                          '' if num_files == 1 else 's'))

    # write out new randomly subsampled csv files from each of the
    # original .csv files
    seen = set()
    for i, fpath in enumerate(file_list):
        if not os.path.isfile(fpath):
            warn('"{}" is not a file!'.format(fpath))
            continue

        df = pd.read_csv(fpath)

        #
        # Remove any runs we have already seen
        #
        df = df[~df['ENA run'].isin(seen)]

        #
        # If we still have too many samples, randomly select
        #
        num_left = df.shape[0]
        if num_max > 0 and num_left > num_max:
            df = df.sample(num_max)

        basename = os.path.basename(fpath)
        print('{:3}: {} ({})'.format(i + 1, basename, df.shape[0]))

        #
        # Remember the runs that we selected
        #
        for run in df['ENA run']:
            seen.add(run)

        outpath = os.path.join(out_dir, basename)

        df.to_csv(outpath, sep=',', encoding='utf-8', index=False)

    print('Done, see outdir "{}"'.format(out_dir))


# --------------------------------------------------
if __name__ == '__main__':
    main()
