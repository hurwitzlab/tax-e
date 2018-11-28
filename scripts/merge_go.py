#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-10-29
Purpose: Merge GO terms for each metagenome into a frequency matrix
"""

import argparse
import csv
import numpy as np
import os
import pandas as pd
import re
import sys
from collections import defaultdict
from goatools import obo_parser


# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='Merge GO terms into a frequence matrix',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'indir', help='Directory of GO counts', metavar='DIR', type=str)

    parser.add_argument(
        '-d',
        '--min_go_depth',
        help='Min depth in GO hierarchy',
        metavar='INT',
        type=int,
        default=0)

    parser.add_argument(
        '-f',
        '--features',
        help='File with feature names (GO terms)',
        metavar='FILE',
        type=str,
        default=None)

    parser.add_argument(
        '-g',
        '--go_file',
        help='go-basic.obo file location',
        metavar='FILE',
        type=str,
        default=os.path.join(os.getcwd(), '../data/go/go-basic.obo'))

    parser.add_argument(
        '-m',
        '--max_samples_per_biome',
        help='Maximum number of samples per biome',
        metavar='INT',
        type=int,
        default=0)

    parser.add_argument(
        '-n',
        '--normalize',
        help='Normalize count: log, tf, nlog_tf, aug_freq',
        metavar='str',
        type=str,
        default=None)

    parser.add_argument(
        '-o',
        '--outfile',
        help='Output matrix file',
        metavar='FILE',
        type=str,
        default='go-freq.csv')

    parser.add_argument(
        '-v',
        '--variance',
        help='Minimum variance to include a feature',
        metavar='FLOAT',
        type=float,
        default=0)

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
        die('"{}" is not a directory'.format(in_dir))

    dirs = []
    for path in os.scandir(in_dir):
        if path.is_dir():
            dirs.append(path.path)

    if not dirs:
        die('Found no subdirectories in "{}"'.format(in_dir))

    return dirs


# --------------------------------------------------
def main():
    """main"""
    args = get_args()
    in_dir = args.indir
    out_file = args.outfile
    min_go_depth = args.min_go_depth
    go_obo = args.go_file
    features_file = args.features
    normalize = args.normalize
    min_variance = args.variance
    max_samples_per_biome = args.max_samples_per_biome

    if not in_dir:
        die('Missing --indir argument')

    if not go_obo:
        die('Missing --go_file')

    if not os.path.isfile(go_obo):
        die('--go_file "{}" is not a file'.format(go_obo))

    warn('Parsing GO {}'.format(go_obo))
    go = obo_parser.GODag(go_obo)

    #
    # Limit the features to those in a given text file
    #
    limit_features = set()
    if features_file:
        regex = re.compile('(GO[_:]\d+)')
        for line in open(features_file, 'rt'):
            match = regex.search(line)
            if match:
                limit_features.add(match.group(0).replace('_', ':'))

    if limit_features:
        warn('Will limit features to {}'.format(len(limit_features)))

    biomes = {}  # will hold biome DF's, keys are biome names
    go_terms = set()  # for all the unique GO terms
    i = 0  # counter for status
    sample_seen = set()  # warn if a sample is duplicated

    dir_list = find_dirs(args.indir)
    if not dir_list:
        die('No directories to work on')

    for biome_dir in dir_list:
        if not os.path.isdir(biome_dir):
            warn('"{}" is not a directory'.format(biome_dir))
            continue

        biome_name = os.path.basename(biome_dir)
        biome_df = pd.DataFrame({'term': []})

        #
        # Find all the files in this dir, merge them into the "biome_df"
        #
        for fnum, file in enumerate(os.scandir(biome_dir)):
            if not file.is_file():
                continue

            if max_samples_per_biome > 0 and fnum + 1 > max_samples_per_biome:
                continue

            if os.stat(file).st_size < 1:
                warn('"{}" is empty!'.format(file.name))
                continue

            # ERR2281809_MERGED_FASTQ_GO.csv => ERR2281809
            run_name = file.name.split('_')[0]
            i += 1
            sys.stdout.write('{:78}\r'.format(
                '{:5}: {} {}'.format(i, biome_name, run_name)))

            if run_name in sample_seen:
                warn('Sample "{}" has been duplicated!'.format(run_name))
                continue
            else:
                sample_seen.add(run_name)

            col_names = ['term', 'desc', 'domain', run_name]
            drop_cols = ['desc', 'domain']

            df = pd.read_csv(
                file.path, names=col_names).drop(
                    drop_cols, axis=1)

            if limit_features:
                df = df[df['term'].isin(limit_features)]

            # Cf. https://en.wikipedia.org/wiki/Tf%E2%80%93idf
            if normalize:
                if normalize == 'log':
                    # Just log as suggested by Prof Morrison
                    df[run_name] = np.log(df[run_name])

                elif normalize == 'tf':
                    # Term frequency by doc length
                    df[run_name] = df[run_name] / df[run_name].sum()

                elif normalize == 'nlog_tf':
                    # Negative log
                    df[run_name] = -1 * np.log(
                        df[run_name] / df[run_name].sum())

                elif normalize == 'aug_freq':
                    # augmented frequency, to prevent a bias towards longer
                    # documents, e.g. raw frequency divided by the raw frequency
                    # of the most occurring term in the document:
                    max_val = df[run_name].max()
                    df[run_name] = 0.5 + (0.5 * df[run_name] / max_val)

                else:
                    die('Unknown normalize: "{}"'.format(normalize))

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
    print()
    go_terms = sorted(go_terms)
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
    # Winnow features/columns (GO terms)
    #
    for term_id in go_terms:
        drop = None
        if term_id in go:
            term = go[term_id]

            if min_go_depth > 0 and term.depth < min_go_depth:
                drop = '({}) depth {} < {}'.format(term.name, term.depth,
                                                   min_go_depth)
            elif limit_features and term_id not in limit_features:
                drop = '({}) not in approved list'.format(term.name)
            elif min_variance > 0 and matrix[term].var() < min_variance:
                drop = '({}) {} variance'.format(term.name, matrix[term].var())
        else:
            drop = 'Unknown term ID'

        if drop:
            print('Dropping {}: {}'.format(term_id, drop))
            matrix.drop(term_id, axis=1, inplace=True)

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

    matrix.index.name = 'sample'

    out_dir = os.path.dirname(out_file)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    matrix.to_csv(out_file, sep=',', header=True, encoding='utf-8')

    #
    # Let the user know how many samples and features made it
    #
    n_rows, n_cols = matrix.shape
    print('Wrote {} rows, {} cols to file {}'.format(n_rows, n_cols, out_file))


# --------------------------------------------------
if __name__ == '__main__':
    main()
