import pandas
import numpy as np
import matplotlib.pyplot as plt

from preprocessing import get_tfidf_matrix
from clustering import apply_dbscan


def main():

    print("Load test data.")
    test_data = load_test_data(nrows=1000)

    print("Create tfidf matrix.")
    tfidf_matrix = get_tfidf_matrix(test_data['TITLE'])
    dense_tfidf_matrix = tfidf_matrix.todense()

    print("Apply dbscan clustering.")
    labels, core_samples_mask = apply_dbscan(dense_tfidf_matrix)

    print("Render plot.")
    plot_cluster(dense_tfidf_matrix, labels, core_samples_mask)


def load_test_data(nrows=None):
    filepath = 'test_data/uci-news-aggregator.csv'
    return pandas.read_csv(filepath, nrows=nrows)


def plot_cluster(original_data, labels, core_samples_mask):
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = original_data[class_member_mask & core_samples_mask] 
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=14)

        xy = original_data[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)

    plt.show()


if __name__ == "__main__":
    main()
