#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.manifold import MDS

infile = '/Users/kyclark/work/tax-e/data/freqs/d1.csv'
X = pd.read_csv(infile)
target = X['target']

X.drop(['sample', 'target'], axis=1, inplace=True)
D = pairwise_distances(X)
D = np.ma.log(D).filled(0)

#plt.imshow(D, zorder=2, cmap='Blues', interpolation='nearest')
#plt.show()

model = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
out = model.fit_transform(D)

#colorize = dict(c=X[:, 0], cmap=plt.cm.get_cmap('Rainbow', 5))

plt.scatter(out[:, 0], out[:, 1]) #, **colorize)
plt.axis('equal')

# tnames = sorted(list(set(target)))
# for i, tname in enumerate(tnames):
#     mask = target == tname
#     print('{} = {}'.format(tname, len(mask[mask])))
#     plt.scatter(out[:, mask][mask], label=tname, alpha=0.5)

plt.show()
