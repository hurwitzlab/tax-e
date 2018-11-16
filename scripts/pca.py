#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-15
Purpose: Rock the Casbah
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from sklearn.decomposition import PCA


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
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

    pca1 = PCA().fit(X)
    plt.plot(np.cumsum(pca1.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance')
    plt.show()

    #pca_half = PCA(0.5).fit(X)
    #n_components = pca_half.n_components_
    #components = pca_half.transform(X)
    #projected = pca_half.inverse_transform(components)

    pca = PCA(n_components=n_components)
    projected = pca.fit_transform(X, target)

    tnames = sorted(list(set(target)))
    for i, tname in enumerate(tnames):
        mask = target == tname
        plt.scatter(
            projected[mask, 0], projected[mask, 1], label=tname, alpha=0.5)

    plt.title('Number of components = {}'.format(n_components))
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')

    plt.legend()
    plt.show()


# --------------------------------------------------
if __name__ == '__main__':
    main()
