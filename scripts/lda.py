#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split

infile = '/Users/kyclark/work/tax-e/data/freqs/d1.csv'
X = pd.read_csv(infile)
target = X['target']

X.drop(['sample', 'target'], axis=1, inplace=True)

cor = np.corrcoef(X)
#print("Pearson cor = {}".format(cor))
plt.imshow(cor)
plt.title('Pearson correlation coefficients')
plt.show()

cov = np.log(np.cov(X))
#print("COV = {}".format(cor))
plt.imshow(cov)
plt.title('Log covariance')
plt.show()

#model = LinearDiscriminantAnalysis()
#iters = 10
#
#predictions = []
#for _ in range(iters):
#    X_train, X_test, y_train, y_test = train_test_split(
#        X, target, test_size=0.33)
#    clf = model.fit(X_train, y_train)
#    predicted = clf.predict(X_test)
#    correct = np.mean(predicted == y_test)
#    print('  {}'.format(correct))
#    predictions.append(correct)
#
#print('Average = {}'.format(np.mean(predictions)))
