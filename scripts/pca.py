#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

infile = '/Users/kyclark/work/tax-e/data/freqs/d1.csv'
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

n_components = 50
pca = PCA(n_components=n_components)
projected = pca.fit_transform(X, target)

tnames = sorted(list(set(target)))
for i, tname in enumerate(tnames):
    mask = target == tname
    plt.scatter(projected[mask, 0], projected[mask, 1], label=tname, alpha=0.5)

plt.title('Number of components = {}'.format(n_components))
plt.xlabel('Component 1')
plt.ylabel('Component 2')

plt.legend()
plt.show()
