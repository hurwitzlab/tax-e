#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-14
Purpose: Rock the Casbah
"""

import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', metavar='str', help='Input file')

    # parser.add_argument(
    #     '-a',
    #     '--arg',
    #     help='A named string argument',
    #     metavar='str',
    #     type=str,
    #     default='')

    parser.add_argument(
        '-i',
        '--iterations',
        help='Number of iterations',
        metavar='int',
        type=int,
        default=10)

    parser.add_argument(
        '-k',
        help='K for KNN',
        metavar='int',
        type=int,
        default=3)

    parser.add_argument(
        '-t',
        '--threshold',
        help='Threshold for variance',
        metavar='float',
        type=float,
        default=0)

    parser.add_argument(
        '-o',
        '--outfile',
        help='File to write plot',
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
def run_model(model, X, target, iters=10):
    predictions = []
    for _ in range(iters):
        X_train, X_test, y_train, y_test = train_test_split(
            X, target, test_size=0.33)
        clf = model.fit(X_train, y_train)
        predicted = clf.predict(X_test)
        correct = np.mean(predicted == y_test)
        #print('  {}'.format(correct))
        predictions.append(correct)

    print('{:.8f} {}'.format(np.mean(predictions), model.__class__.__name__))


# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()
    infile = args.file
    iters = args.iterations
    var_thresh = args.threshold

    if var_thresh > 1 or var_thresh < 0:
        die('--threshold {} must be between 0 and 1')

    X = pd.read_csv(infile)
    target = X['target']
    X.drop(['sample', 'target'], axis=1, inplace=True)

    if var_thresh > 0:
        n_features = X.shape[1]
        sel = VarianceThreshold(threshold=var_thresh)
        X = sel.fit_transform(X)
        print('Using threshold {} reduced features from {} to {}'.format(
            var_thresh, n_features, X.shape[1]))

    models = [
        MultinomialNB(),
        DecisionTreeClassifier(),
        LinearSVC(),
        LogisticRegression(random_state=0),
        RandomForestClassifier(n_estimators=100, random_state=0),
        KNeighborsClassifier(n_neighbors=args.k)
    ]

    entries = []
    for model in models:
        model_name = model.__class__.__name__
        accuracies = cross_val_score(
            model, X, target, scoring='accuracy', cv=iters)
        print('{:8f} {}'.format(np.mean(accuracies), model_name))
        for fold_idx, accuracy in enumerate(accuracies):
            entries.append((model_name, fold_idx, accuracy))

    cv_df = pd.DataFrame(
        entries, columns=['model_name', 'fold_idx', 'accuracy'])
    sns.boxplot(x='model_name', y='accuracy', data=cv_df)
    sns.stripplot(
        x='model_name',
        y='accuracy',
        data=cv_df,
        size=8,
        jitter=True,
        edgecolor="gray",
        linewidth=2)
    plt.xticks(rotation=30, ha='right')
    plt.gcf().subplots_adjust(bottom=.3, left=.2)

    if args.outfile:
        print('Writing figure to "{}"'.format(args.outfile))
        plt.savefig(args.outfile)

    plt.show()


# --------------------------------------------------
if __name__ == '__main__':
    main()
