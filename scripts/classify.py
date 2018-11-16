#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@email.arizona.edu>
Date   : 2018-11-07
Purpose: Train/test
"""

import argparse
import itertools
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='Use frequency matrix to train/test',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', metavar='str', help='Input file')

    parser.add_argument(
        '-o',
        '--outfile',
        help='File to write confusion matrix image',
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
    infile = args.file

    X = pd.read_csv(infile, sep=',', header=0)
    target = X['target']
    X.drop(['sample', 'target'], axis=1, inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, target, test_size=0.33)

    clf = MultinomialNB().fit(X_train, y_train)
    predicted = clf.predict(X_test)
    print('Predicting with {} accuracy'.format(np.mean(predicted == y_test)))

    tnames = sorted(list(set(target)))

    # for i, tname in enumerate(tnames):
    #     print(tname)
    #     coef = list(zip(X.columns, clf.coef_[i]))
    #     print(coef)

    cnf = confusion_matrix(predicted, y_test, labels=tnames)
    plot_confusion_matrix(cnf, tnames, outfile=args.outfile)


# --------------------------------------------------
def plot_confusion_matrix(cm,
                          classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues,
                          outfile=None):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    #
    # This is generic matplotlib code to draw matrix
    #
    # plt.imshow(cm, interpolation='nearest', cmap=cmap)
    # plt.title(title)
    # plt.colorbar()
    # tick_marks = np.arange(len(classes))
    # plt.xticks(tick_marks, classes, rotation=45)
    # plt.yticks(tick_marks, classes)

    # fmt = '.2f' if normalize else 'd'
    # thresh = cm.max() / 2.
    # for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    #     plt.text(
    #         j,
    #         i,
    #         format(cm[i, j], fmt),
    #         horizontalalignment="center",
    #         color="white" if cm[i, j] > thresh else "black")

    # plt.ylabel('True label')
    # plt.xlabel('Predicted label')
    # plt.tight_layout()

    #
    # Seaborn method is maybe prettier?
    # Need to manually rotate x labels and enlarge margins to see them
    #
    cm_plt = sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='YlGnBu',
        xticklabels=classes,
        yticklabels=classes)
    plt.setp(cm_plt.get_xticklabels(), rotation=45, ha='right')
    plt.gcf().subplots_adjust(bottom=.2, left=.2)

    #
    # Option to save figure
    #
    if outfile:
        print('Saving confusion matrix to "{}"'.format(outfile))
        plt.savefig(outfile)

    plt.show()


# --------------------------------------------------
if __name__ == '__main__':
    main()
