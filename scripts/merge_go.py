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
        default='')

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

    if not in_dir:
        die('Missing --indir argument')

    if not os.path.isdir(in_dir):
        die('--indir "{}" is not a directory'.format(in_dir))

    biomes = {}  # will hold biome DF's, keys are biome names
    go_terms = set()  # for all the unique GO terms
    i = 0  # counter for status

    for biome_dir in find_dirs(args.indir):
        biome_name = biome_dir.name  # e.g., gut, wastewater
        biome_df = pd.DataFrame({'term': []})

        #
        # Find all the files in this dir, merge them into the "biome_df"
        #
        for file in os.scandir(biome_dir):
            if not file.is_file():
                continue

            if os.stat(file).st_size < 1:
                warn('"{}" is empty!'.format(file.name))
                continue

            # ERR2281809_MERGED_FASTQ_GO.csv => ERR2281809
            run_name = file.name.split('_')[0]
            i += 1
            print("{:3}: {} {}".format(i, biome_name, run_name))

            col_names = ['term', 'desc', 'domain', run_name]
            drop_cols = ['desc', 'domain']

            df = pd.read_csv(
                file.path, names=col_names).drop(
                    drop_cols, axis=1)
            df.set_index('term')

            if args.normalize:
                df[run_name] = df[run_name] / df[run_name].sum()

            biome_df = pd.merge(biome_df, df, on='term', how='outer').fillna(0)

        #
        # Take note of all the GO terms we saw
        #
        for term in biome_df['term']:
            go_terms.add(term)

        biomes[biome_name] = biome_df

    #
    # Create a new empty matrix with all the GO terms
    #
    go_terms = sorted(list(go_terms))
    print('{} go terms'.format(len(go_terms)))
    matrix = pd.DataFrame({'term': go_terms})

    #
    # Merge all the biomes and GO terms
    #
    for biome_name, biome_df in biomes.items():
        print('Merging {}'.format(biome_name))
        matrix = pd.merge(matrix, biome_df, on='term', how='outer').fillna(0)

    #
    # Transpose the matrix and drop the "term" row/index
    #
    matrix = matrix.T.drop('term')
    matrix.columns = go_terms

    #
    # Create a new "target" column and set using columns from the biome DFs
    #
    print('Setting targets')
    matrix['target'] = 'NA'
    for biome_name, biome_df in biomes.items():
        for col in biome_df.columns:
            if col == 'term':
                continue
            matrix.loc[col, 'target'] = biome_name

    #matrix = matrix.reset_index(drop=True)
    matrix.index.name = 'sample'
    matrix.to_csv(out_file, sep=',', header=True, encoding='utf-8')

    print('Done, see output file {}'.format(out_file))


# --------------------------------------------------
if __name__ == '__main__':
    main()
