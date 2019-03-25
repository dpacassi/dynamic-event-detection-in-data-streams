import pandas
import numpy as np
import matplotlib.pyplot as plt
import collections

from preprocessing import get_tfidf_matrix
from sklearn.metrics import accuracy_score, completeness_score, v_measure_score
from clustering import (
    apply_dbscan,
    apply_meanshift,
    apply_affinity_propagation,
    apply_birch,
)


def main():

    print("Load test data.")
    test_data = load_test_data(nrows=1000)

    print("Create tfidf matrix.")
    tfidf_matrix, features = get_tfidf_matrix(test_data["TITLE"])

    print("Cluster data.")

    print("------------------------------")
    print("DBSCAN:")
    run_clustering_algorithm(apply_dbscan, test_data, tfidf_matrix, features)

    print("------------------------------")
    print("Affinity Propagation:")
    run_clustering_algorithm(apply_affinity_propagation, test_data, tfidf_matrix, features)

    print("------------------------------")
    print("Birch:")
    run_clustering_algorithm(apply_birch, test_data, tfidf_matrix, features)

    # print('------------------------------')
    # print("Meanshift:")
    # run_clustering_algorithm(apply_meanshift, test_data, tfidf_matrix.todense(), features, False)


def run_clustering_algorithm(algorithm, test_data, tfidf_matrix, features, show_details=False):
    labels = algorithm(tfidf_matrix)
    generate_report(labels, test_data, tfidf_matrix, features, show_details)


def generate_report(labels, test_data, tfidf_matrix, features, show_details=True):
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)

    cluster_set = set(test_data["STORY"])
    actual_clusters = len(cluster_set)

    cluster_dict = {}
    for index, cluster in enumerate(cluster_set):
        cluster_dict[cluster] = index

    labels_true = []
    for story in test_data["STORY"].values:
        labels_true.append(cluster_dict[story])

    grouped_indices = collections.defaultdict(list)
    for index, value in enumerate(labels):
        if value >= 0:
            grouped_indices[value].append(index)

    if show_details:
        for key, indices in grouped_indices.items():
            print("Group %d: \n" % key)
            print(indices)
            for index in indices:
                print(test_data["ID"][index])
                print(test_data["TITLE"][index])
                print(get_features_from_matrix(tfidf_matrix[index].todense(), features))
            print("------------------------------")

    print("Actual number of clusters: %d" % actual_clusters)
    print("Estimated number of clusters: %d" % n_clusters)
    print("Estimated number of noise points: %d" % n_noise)

    print("Completeness: %0.3f" % completeness_score(labels_true, labels))
    print("V-measure: %0.3f" % v_measure_score(labels_true, labels))


def get_features_from_matrix(matrix, features):
    actual_features = []
    for index, value in enumerate(matrix.A1):
        if value > 0:
            actual_features.append(features[index])

    return actual_features


def load_test_data(nrows=None):
    filepath = "test_data/uci-news-aggregator.csv"
    return pandas.read_csv(filepath, nrows=nrows)


if __name__ == "__main__":
    main()
