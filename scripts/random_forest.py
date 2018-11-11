#!/usr/bin/env python3

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def main():
    infile = '/Users/kyclark/work/tax-e/data/freqs/d1.csv'
    X = pd.read_csv(infile)
    target = X['target']
    X.drop(['sample', 'target'], axis=1, inplace=True)

    run_model('Decision Tree', DecisionTreeClassifier(), X, target)
    run_model('Random Forest',
              RandomForestClassifier(n_estimators=100, random_state=0), X,
              target)


def run_model(model_name, model, X, target, iters=10):
    print(model_name)
    predictions = []
    for _ in range(iters):
        X_train, X_test, y_train, y_test = train_test_split(
            X, target, test_size=0.33)
        clf = model.fit(X_train, y_train)
        predicted = clf.predict(X_test)
        correct = np.mean(predicted == y_test)
        print('  {}'.format(correct))
        predictions.append(correct)

    print('Average = {}'.format(np.mean(predictions)))


main()
