#!/usr/bin/env python3
"""
Author : Ken Youens-Clark
Date   : 2018-11-16
Purpose: Plot the number of features
"""

import argparse
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Plot the number of features in input files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'files', nargs='+', metavar='FILE', help='Input files')

    parser.add_argument(
        '-o',
        '--outfile',
        help='Save figure to output file',
        metavar='str',
        type=str,
        default=None)

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
    """Make a jazz noise here"""
    args = get_args()
    files = args.files
    out_file = args.outfile

    n = []
    names = []
    for file in files:
        print(file)
        X = pd.read_csv(file)
        target = X['target']
        X.drop(['sample', 'target'], axis=1, inplace=True)
        n.append(X.shape[1])
        names.append(os.path.basename(file))

    #fig, ax = plt.subplots()
    plt.bar(names, n)
    plt.xticks(rotation=30, ha='right')
    #plt.setp(plt.get_xticklabels(), rotation=45, ha='right')
    plt.gcf().subplots_adjust(bottom=.2, left=.2)
    plt.ylabel('Number of features')
    plt.xlabel('File')

    if out_file:
        warn('Saving to "{}"'.format(out_file))
        plt.savefig(out_file)

    plt.show()


# --------------------------------------------------
if __name__ == '__main__':
    main()
