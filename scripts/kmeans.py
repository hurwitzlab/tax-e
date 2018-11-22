#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-15
Purpose: Kmeans clustering
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sys
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Kmeans clustering',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', nargs='+', metavar='FILE', help='Input file')

    parser.add_argument(
        '-a',
        '--algorithm',
        help='K-means algorithm ("auto", "full" or "elkan")',
        metavar='str',
        type=str,
        default='auto')

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
        default=10)

    parser.add_argument(
        '-v',
        '--view_cnf',
        help='View confusion matrix',
        action='store_true',
        default=False)

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
    n_components = args.components
    iterations = args.iterations

    for infile in args.file:
        X = pd.read_csv(infile)
        target = X['target']
        X.drop(['sample', 'target'], axis=1, inplace=True)
        tfactors = target.factorize()
        labels = tfactors[0] + 1  # move up from zero-offset
        n_clusters = len(tfactors[1])

        predicted = KMeans(
            n_clusters=n_clusters,
            algorithm=args.algorithm,
            max_iter=iterations).fit_predict(X)

        # predicted = SpectralClustering(
        #     n_clusters=n_clusters,
        #     affinity='nearest_neighbors',
        #     assign_labels='kmeans').fit_predict(X)

        print('{:.02f} {} ({}, {})'.format(
            np.mean(predicted == labels), os.path.basename(infile), X.shape[0],
            X.shape[1]))

        if args.view_cnf:
            cnf = confusion_matrix(predicted, labels)
            cm_plt = sns.heatmap(
                cnf,
                annot=True,
                fmt='d',
                cmap='YlGnBu',
                xticklabels=tfactors[1],
                yticklabels=tfactors[1])

            plt.setp(cm_plt.get_xticklabels(), rotation=45, ha='right')
            plt.gcf().subplots_adjust(bottom=.2, left=.2)
            plt.title(os.path.basename(infile))
            plt.show()


# --------------------------------------------------
if __name__ == '__main__':
    main()
