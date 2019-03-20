import numpy as np

from sklearn.cluster import DBSCAN, Birch, MeanShift


def apply_dbscan(x):
    # https://scikit-learn.org/stable/modules/clustering.html#dbscan
    # https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
    dbscan = DBSCAN(eps=3, min_samples=2).fit(x)
    core_samples_mask = np.zeros_like(dbscan.labels_, dtype=bool)
    core_samples_mask[dbscan.core_sample_indices_] = True
    labels = dbscan.labels_

    return labels, core_samples_mask


def apply_birch(x):
    # https://scikit-learn.org/stable/modules/clustering.html#birch
    return Birch(branching_factor=50, n_clusters=None, threshold=0.5, compute_labels=True).fit(x)


def apply_meanshift(x):
    # https://scikit-learn.org/stable/modules/clustering.html#mean-shift
    return MeanShift(bandwidth=2).fit(x)