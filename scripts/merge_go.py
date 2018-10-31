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

    matrix = {}
    for i, file in enumerate(os.listdir(in_dir)):
        # ERR2281809_MERGED_FASTQ_GO.csv => ERR2281809
        sample = file.split('_')[0]

        # initialize matrix for sample
        matrix[sample] = {}

        print("{:3}: {}".format(i, sample))

        with open(os.path.join(in_dir, file)) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')# newline='')
            for row in reader:
                go, count = row[0], row[-1]
                matrix[sample][go] = count

    uniq_go = set()
    for sample in matrix.keys():
        for go in matrix[sample].keys():
            uniq_go.add(go)

    sorted_go = sorted(uniq_go)
    sorted_samples = sorted(matrix.keys())

    out_fh = open(out_file, 'wt')
    out_fh.write(','.join([''] + sorted_samples) + '\n')

    for go in sorted_go:
        counts = []
        for sample in sorted_samples:
            counts.append(matrix[sample][go] if go in matrix[sample] else '0')

        out_fh.write(','.join([go] + counts) + '\n')

    out_fh.close()

    print('Done')

# --------------------------------------------------
if __name__ == '__main__':
    main()
