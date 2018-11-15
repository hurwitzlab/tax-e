#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-14
Purpose: Rock the Casbah
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from goatools import obo_parser
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Latent Dirichlet',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', metavar='str', help='Input file')

    parser.add_argument(
        '-c',
        '--number_components',
        help='Number of components',
        metavar='int',
        type=int,
        default=0)

    parser.add_argument(
        '-i',
        '--iters',
        help='Number of iterations',
        metavar='int',
        type=int,
        default=5)

    parser.add_argument(
        '-n',
        '--number_topics',
        help='Number of topics to display',
        metavar='int',
        type=int,
        default=10)

    parser.add_argument(
        '-t',
        '--threshold',
        help='Threshold for variance',
        metavar='float',
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
def display_topics(model, feature_names, no_top_words):
    go_obo = '/Users/kyclark/work/tax-e/data/go/go-basic.obo'
    go = obo_parser.GODag(go_obo)

    for topic_idx, topic in enumerate(model.components_):
        terms = [
            feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]
        ]

        print("Topic {:d}:".format(topic_idx))

        for i, term in enumerate(terms):
            if term in go:
                go_term = go[term]
                print('{:2} {} ({}) = {} {}'.format(
                    i + 1, term, go_term.namespace, go_term.name,
                    len(go_term.parents)))
        print()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()
    infile = args.file
    var_thresh = args.threshold

    X = pd.read_csv(infile)
    target = X['target']
    X.drop(['sample', 'target'], axis=1, inplace=True)

    #
    # This doesn't work because X becomes an np.ndarray and so
    # we lose the column headers which is needed for topic names
    #
    # if var_thresh > 0:
    #     n_features = X.shape[1]
    #     sel = VarianceThreshold(threshold=var_thresh)
    #     X = sel.fit_transform(X)
    #     print('Using threshold {} reduced features from {} to {}'.format(
    #         var_thresh, n_features, X.shape[1]))

    n_components = args.number_components
    if n_components == 0:
        n_components = len(target.factorize()[1])

    lda = LatentDirichletAllocation(
        n_components=n_components,
        max_iter=args.iters,
        random_state=0,
        learning_method='batch').fit(X)

    display_topics(lda, X.columns, args.number_topics)

    # X_new = LatentDirichletAllocation(
    #     n_components=n_components,
    #     max_iter=5,
    #     random_state=0,
    #     learning_method='batch').fit_transform(X)
    # print(X_new)

    #test_model(X, name='X')
    #test_model(X_new, name='X_new')


# --------------------------------------------------
def test_model(X, name='model', iters=10):
    preds = []
    for _ in range(iters):
        X_train, X_test, y_train, y_test = train_test_split(
            X, target, test_size=0.33)
        clf = MultinomialNB().fit(X_train, y_train)
        predicted = clf.predict(X_test)
        accuracy = np.mean(predicted == y_test)
        preds.append(accuracy)
        print('Predicting with {} accuracy'.format(accuracy))

    print('Average {}'.format(np.mean(preds)))


# --------------------------------------------------
if __name__ == '__main__':
    main()
