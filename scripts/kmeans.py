#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-15
Purpose: Kmeans clustering
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from sklearn.cluster import KMeans


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Kmeans clustering',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', metavar='FILE', help='Input file')

    parser.add_argument(
        '-c',
        '--components',
        help='Number of components',
        metavar='int',
        type=int,
        default=2)

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
    infile = args.file
    n_components = args.components

    X = pd.read_csv(infile)
    target = X['target']
    X.drop(['sample', 'target'], axis=1, inplace=True)
    tfactors = target.factorize()

    kmeans = KMeans(n_clusters=len(tfactors[1])).fit(X)
    predicted = kmeans.predict(X)
    print(predicted)
    print(tfactors[0])

    print(np.mean(predicted == tfactors[0]))


# --------------------------------------------------
if __name__ == '__main__':
    main()
