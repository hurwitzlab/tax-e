#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA

def plot_digits(data, title=''):
    fig, axes = plt.subplots(4, 10, figsize=(10, 4),
                             subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))

    for i, ax in enumerate(axes.flat):
        ax.imshow(data[i].reshape(8,8),
                  cmap='binary', interpolation='nearest',
                  clim=(0, 16))

    plt.show()

def main():
    digits = load_digits()

    #pca = PCA(2)
    #projected = pca.fit_transform(digits.data)
    #plt.scatter(projected[:, 0], projected[:, 1],
    #            c=digits.target, edgecolor='none', alpha=0.5,
    #            cmap=plt.cm.get_cmap('Spectral', 10))
    #plt.xlabel('Component 1')
    #plt.ylabel('Component 2')
    #plt.colorbar()
    #plt.show()

    plot_digits(digits.data)

    np.random.seed(42)
    noisy = np.random.normal(digits.data, 4)
    plot_digits(noisy)

    pca = PCA(0.5).fit(noisy)
    print('n comp = {}'.format(pca.n_components_))

    components = pca.transform(noisy)
    filtered = pca.inverse_transform(components)
    plot_digits(filtered)

main()
