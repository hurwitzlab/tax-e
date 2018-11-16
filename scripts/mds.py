#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-15
Purpose: MDS
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from sklearn.manifold import MDS
from sklearn.metrics import pairwise_distances


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='MDS',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', metavar='FILE', help='Input file')

    parser.add_argument(
        '-o',
        '--outfile',
        help='Save figure to output file',
        metavar='FILE',
        type=str,
        default=None)

    parser.add_argument(
        '-c',
        '--components',
        help='Number of components',
        metavar='int',
        type=int,
        default=2)

    parser.add_argument(
        '-i',
        '--iterations',
        help='Number of iterations',
        metavar='int',
        type=int,
        default=300)

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
    in_file = args.file
    out_file = args.outfile
    n_components = args.components
    iterations = args.iterations

    X = pd.read_csv(in_file)
    target = X['target']

    X.drop(['sample', 'target'], axis=1, inplace=True)
    D = pairwise_distances(X)
    D = np.ma.log(D).filled(0)

    model = MDS(
        n_components=n_components,
        dissimilarity='precomputed',
        max_iter=iterations)

    out = model.fit_transform(D)

    plt.scatter(out[:, 0], out[:, 1], c=target.factorize()[0])  #, **colorize)
    plt.axis('equal')

    if out_file:
        plt.savefig(out_file)
        warn('Saved plot to "{}"'.format(out_file))

    plt.show()


# --------------------------------------------------
if __name__ == '__main__':
    main()
