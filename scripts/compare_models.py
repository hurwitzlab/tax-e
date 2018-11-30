#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-14
Purpose: Compare various models on data
"""

import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
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
        description='Compare various models on data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', metavar='str', help='Input file')

    parser.add_argument(
        '-i',
        '--iterations',
        help='Number of iterations',
        metavar='int',
        type=int,
        default=10)

    parser.add_argument(
        '-k', help='K for KNN', metavar='int', type=int, default=3)

    parser.add_argument(
        '-v',
        '--variance',
        help='Minimum variance (0 < n < 1)',
        metavar='float',
        type=float,
        default=0)

    parser.add_argument(
        '-t',
        '--title',
        help='Title for plot',
        metavar='str',
        type=str,
        default=None)

    parser.add_argument(
        '-o',
        '--outfile',
        help='File to write comparison plot',
        metavar='str',
        type=str,
        default=None)

    parser.add_argument(
        '-s',
        '--save_cnf',
        help='Save confusion matrix plots',
        action='store_true')

    parser.add_argument(
        '-e',
        '--eliminate',
        help='Use RFE to eliminate features',
        action='store_true')

    parser.add_argument(
        '-q',
        '--quiet',
        help='Be quiet/do not show plots',
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
def main():
    """Make a jazz noise here"""
    args = get_args()
    infile = args.file
    iterations = args.iterations
    var_thresh = args.variance

    if var_thresh > 1 or var_thresh < 0:
        die('--threshold {} must be between 0 and 1')

    X = pd.read_csv(infile)
    target = X['target']
    X.drop(['sample', 'target'], axis=1, inplace=True)
    tfactors = target.factorize()

    if var_thresh > 0:
        n_features = X.shape[1]
        sel = VarianceThreshold(threshold=var_thresh)
        X = sel.fit_transform(X)
        print('Using threshold {} reduced features from {} to {}'.format(
            var_thresh, n_features, X.shape[1]))

    models = [
        MultinomialNB(),
        KNeighborsClassifier(n_neighbors=args.k),
        LogisticRegression(),
        LinearSVC(),
        DecisionTreeClassifier(),
        RandomForestClassifier(n_estimators=100),
    ]

    entries = []
    tnames = sorted(list(set(target)))

    for model in models:
        model_name = model.__class__.__name__

        if not args.quiet:
            print('Model "{}"'.format(model_name))

        # accuracies = cross_val_score(
        #     model, X, target, scoring='accuracy', cv=iterations)
        # print('{:8f} {}'.format(np.mean(accuracies), model_name))
        # for fold_idx, accuracy in enumerate(accuracies):
        #     entries.append((model_name, fold_idx, accuracy))

        if args.eliminate:
            print('Using RFE!')
            model = RFE(model, 5, step=1)

        for i in range(iterations):
            X_train, X_test, y_train, y_test = train_test_split(
                X, target, test_size=0.33)

            clf = model.fit(X_train, y_train)
            predicted = clf.predict(X_test)
            entries.append((model_name, i, np.mean(predicted == y_test)))


        # cnf = confusion_matrix(predicted, y_test, labels=tnames)
        #print(cnf)
        # plot_confusion_matrix(
        #     cnf=cnf,
        #     title=model_name,
        #     classes=tnames,
        #     savefigs=args.save_cnf,
        #     quiet=args.quiet)

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

    if args.title:
        plt.title(args.title)

    plt.gcf().subplots_adjust(bottom=.3, left=.2)

    if args.outfile:
        print('Writing figure to "{}"'.format(args.outfile))
        plt.savefig(args.outfile)

    if not args.quiet:
        plt.show()


# --------------------------------------------------
def plot_confusion_matrix(cnf,
                          classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues,
                          savefigs=False,
                          quiet=False):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cnf = cm.astype('float') / cnf.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    #
    # Seaborn method is maybe prettier?
    # Need to manually rotate x labels and enlarge margins to see them
    #
    cm_plt = sns.heatmap(
        cnf,
        annot=True,
        fmt='d',
        cmap='YlGnBu',
        xticklabels=classes,
        yticklabels=classes)

    plt.setp(cm_plt.get_xticklabels(), rotation=45, ha='right')
    plt.gcf().subplots_adjust(bottom=.2, left=.2)
    plt.title(title)

    if savefigs:
        outfile = 'cnf-' + title.lower().replace(' ', '_') + '.png'
        print('Saving confusion matrix to "{}"'.format(outfile))
        plt.savefig(outfile)

    if not quiet:
        plt.show()


# --------------------------------------------------
if __name__ == '__main__':
    main()
