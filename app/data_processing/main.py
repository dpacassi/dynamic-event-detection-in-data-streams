import pandas
import numpy as np
import matplotlib.pyplot as plt
import collections

from preprocessing import get_tfidf_matrix
from sklearn.metrics import accuracy_score
from clustering import apply_dbscan, apply_meanshift


def main():

    print("Load test data.")
    test_data = load_test_data(nrows=1000)

    print("Create tfidf matrix.")
    tfidf_matrix, features = get_tfidf_matrix(test_data['TITLE'])
    # dense_tfidf_matrix = tfidf_matrix.todense()

    print("Cluster data.")
    # labels, core_samples_mask = apply_dbscan(dense_tfidf_matrix)
    labels = apply_dbscan(tfidf_matrix)

    print("Generate Report.")
    print('------------------------------')

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)

    actual_clusters = len(set(test_data['STORY']))
    difference = abs(actual_clusters - n_clusters)

    grouped_indices = collections.defaultdict(list)
    for index, value in enumerate(labels):
        if value >= 0:
            grouped_indices[value].append(index)

    for key, indices in grouped_indices.items():
        print('Group %d: \n' % key)
        print(indices)
        for index in indices:
            print(test_data['ID'][index])
            print(test_data['TITLE'][index])
            print(get_features_from_matrix(tfidf_matrix[index].todense(), features))
        print('------------------------------')

    print('Actual number of clusters: %d' % actual_clusters)
    print('Estimated number of clusters: %d' % n_clusters)
    print('Estimated number of noise points: %d' % n_noise)
    print('Difference: %f' % difference)


def get_features_from_matrix(matrix, features):
    actual_features = []
    for index, value in enumerate(matrix.A1):
        if value > 0:
            actual_features.append(features[index])

    return actual_features


def load_test_data(nrows=None):
    filepath = 'test_data/uci-news-aggregator.csv'
    return pandas.read_csv(filepath, nrows=nrows)


if __name__ == "__main__":
    main()
