#!/usr/bin/env python3
"""
Author : kyclark
Date   : 2018-11-14
Purpose: Latent Dirichlet Allocation to discover topics and important features
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
from goatools import obo_parser
from scipy.stats import mode
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description=
        'Latent Dirichlet Allocation to discover topics and important features',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', nargs='+', metavar='str', help='Input file')

    parser.add_argument(
        '-c',
        '--number_components',
        help='Number of components',
        metavar='int',
        type=int,
        default=0)

    parser.add_argument(
        '-g',
        '--go_file',
        help='go-basic.obo file location',
        metavar='FILE',
        type=str,
        default=os.path.join(os.getcwd(), '../data/go/go-basic.obo'))

    parser.add_argument(
        '-i',
        '--iterations',
        help='Number of iterations',
        metavar='int',
        type=int,
        default=10)

    parser.add_argument(
        '-m',
        '--min_confidence',
        help='Minimun confidence for topic assignment (0<n<1)',
        metavar='float',
        type=float,
        default=0.)

    parser.add_argument(
        '-n',
        '--number_topics',
        help='Number of topics to display',
        metavar='int',
        type=int,
        default=10)

    parser.add_argument(
        '-o',
        '--outfile',
        help='Write GO terms to output file',
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
def display_topics(model, feature_names, no_top_words, go_file):
    """
    Params:
    - model (LDA)
    - feature names/targets
    - number of top "words" (GO terms) to display for each topic
    Returns:
    - sorted, unique list of GO terms
    """
    go = obo_parser.GODag(go_file)
    all_terms = set()

    for topic_idx, topic in enumerate(model.components_):
        terms = [
            feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]
        ]

        print("Topic {:d}:".format(topic_idx + 1))

        for i, term in enumerate(terms):
            if term in go:
                go_term = go[term]
                all_terms.add(term)
                print('{:2} {} ({}) = {} [{}]'.format(
                    i + 1, term, go_term.namespace, go_term.name,
                    go_term.depth))
        print()

    return list(sorted(all_terms))


# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()
    out_file = args.outfile
    iterations = args.iterations
    go_file = args.go_file
    min_confidence = args.min_confidence

    if min_confidence > 1:
        min_confidence /= 100

    if min_confidence < 0:
        die('--min_confidence "{}" cannot be < 0'.format(min_confidence))

    if not go_file:
        die('Missing --go_file')

    if not os.path.isfile(go_file):
        die('--go_file "{}" is not a file'.format(go_file))

    for infile in args.file:
        print('>>>>>>{}'.format(os.path.basename(infile)))
        X = pd.read_csv(infile)
        target = X['target']
        tfactors = target.factorize()
        X.drop(['sample', 'target'], axis=1, inplace=True)

        #
        # The number of components (topics) can be given
        # by the user or inferred from the data (the distinct
        # number of targets)
        #
        n_components = args.number_components
        if n_components == 0:
            n_components = len(tfactors[1])

        model = LatentDirichletAllocation(
            n_components=n_components,
            max_iter=iterations,
            random_state=0,
            learning_method='batch')
        lda = model.fit(X)

        terms = display_topics(lda, X.columns, args.number_topics, go_file)

        doc_topic_distr = lda.transform(X)
        #print(doc_topic_distr)
        predicted = []
        for i, topic in enumerate(doc_topic_distr):
            best_topic_idx = np.argmax(topic)
            confidence = topic[best_topic_idx]
            if confidence >= min_confidence:
                predicted.append(best_topic_idx)
            else:
                predicted.append(-1)

            #print('{} = topic {} ({}%)'.format(i + 1, best_topic_idx + 1,
            #                                   confidence))

        predicted = np.array(predicted)
        target_indexes = tfactors[0]
        print('Topic assigment with min_confidence {}%'.format(
            int(min_confidence * 100)))

        for target_idx in set(target_indexes):
            #
            # Find the predicted values for the target
            #
            subset = predicted[target_indexes == target_idx]

            #
            # Find mode/accuracy when mode >= 0
            #
            class_mode = mode(subset).mode[0] # if len(subset_ok) > 0 else -1
            accuracy = np.mean(subset == class_mode) if class_mode >= 0 else 0
            #accuracy = accuracy_score(subset, class_mode)

            print('{:6} {:>3}% ({:3}/{:3} == {:3})'.format(
                target_idx + 1, int(accuracy * 100), np.sum(subset == class_mode),
                len(subset), class_mode))

        #for t, p in zip(tfactors[0], predicted):
        #    print('{}\t{}'.format(t, p))

        if out_file:
            fh = open(out_file, 'wt')
            fh.write('\n'.join(terms) + '\n')
            fh.close()

        # accuracies = cross_val_score(
        #     lda, X, target, scoring='accuracy', cv=iterations)
        # print('{:8f} {}'.format(np.mean(accuracies), model_name))
        # for fold_idx, accuracy in enumerate(accuracies):
        #     entries.append((model_name, fold_idx, accuracy))

        # X_new = LatentDirichletAllocation(
        #     n_components=n_components,
        #     max_iter=iterations,
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
