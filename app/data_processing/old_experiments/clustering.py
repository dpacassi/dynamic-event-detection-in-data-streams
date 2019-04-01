import numpy as np
import hdbscan

from sklearn.cluster import DBSCAN, Birch, MeanShift, AffinityPropagation, OPTICS


def apply_dbscan(x):
    # https://scikit-learn.org/stable/modules/clustering.html#dbscan
    # https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
    return DBSCAN(eps=0.5, min_samples=4).fit_predict(x)


def apply_hdbscan(x):
    # https://github.com/scikit-learn-contrib/hdbscan/blob/master/hdbscan/hdbscan_.py#L338
    return hdbscan.HDBSCAN(
        min_cluster_size=4,
        metric='cosine'
    ).fit_predict(x)


def apply_optics(x):
    # https://scikit-learn.org/dev/modules/generated/sklearn.cluster.OPTICS.html
    return OPTICS(eps=0.5, min_samples=4).fit_predict(x)


def apply_affinity_propagation(x):
    # https://scikit-learn.org/stable/modules/clustering.html#affinity-propagation
    return AffinityPropagation(
        affinity="euclidean",
        convergence_iter=15,
        copy=True,
        damping=0.5,
        max_iter=200,
        preference=None,
        verbose=False,
    ).fit_predict(x)


def apply_birch(x):
    # https://scikit-learn.org/stable/modules/clustering.html#birch
    return Birch(
        branching_factor=50, n_clusters=None, threshold=0.5, compute_labels=True
    ).fit_predict(x)


def apply_meanshift(x):
    # https://scikit-learn.org/stable/modules/clustering.html#mean-shift
    return MeanShift().fit_predict(x)