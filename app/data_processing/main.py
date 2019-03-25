import pandas
import numpy as np
import matplotlib.pyplot as plt
import collections

from sklearn.metrics import accuracy_score, completeness_score, v_measure_score

from preprocessing import (
    extract_entities,
    extract_tokens,
    get_tfidf_matrix,
    get_hash_matrix,
    get_count_matrix,
)
from clustering import (
    apply_dbscan,
    apply_optics,
    apply_meanshift,
    apply_affinity_propagation,
    apply_birch,
)


def main():

    print("Load test data.")
    test_data = load_test_data(nrows=1000)

    print("Create data matrices.")
    text = test_data["TITLE"]

    tfidf_matrix, features = get_tfidf_matrix(text)
    hash_matrix, features = get_hash_matrix(text)

    raw_count_matrix, features = get_count_matrix(text)
    entity_count_matrix, features = get_count_matrix(text, extract_entities)
    token_count_matrix, features = get_count_matrix(text, extract_tokens)

    print("Cluster data.")

    print("------------------------------")
    print("DBSCAN:")
    run_algorithm_with_different_vectorizer(
        apply_dbscan,
        test_data,
        features,
        hash_matrix,
        raw_count_matrix,
        entity_count_matrix,
        token_count_matrix,
        tfidf_matrix
    )

    print("------------------------------")
    print("OPTICS:")
    run_algorithm_with_different_vectorizer(
        apply_optics,
        test_data,
        features,
        hash_matrix=None,
        raw_count_matrix=None,
        entity_count_matrix=None,
        token_count_matrix=token_count_matrix.toarray(),
        tfidf_matrix=None
    )

    print("------------------------------")
    print("Affinity Propagation:")
    run_clustering_algorithm(
        apply_affinity_propagation, test_data, tfidf_matrix, features
    )

    print("------------------------------")
    print("Birch:")
    run_clustering_algorithm(apply_birch, test_data, tfidf_matrix, features)

    # print('------------------------------')
    # print("Meanshift:")
    # run_clustering_algorithm(apply_meanshift, test_data, tfidf_matrix.todense(), features, False)


def run_algorithm_with_different_vectorizer(
    algorithm,
    test_data,
    features,
    hash_matrix,
    raw_count_matrix,
    entity_count_matrix,
    token_count_matrix,
    tfidf_matrix
):
    if hash_matrix is not None:
        print("Using HashVectorizer")
        run_clustering_algorithm(algorithm, test_data, hash_matrix, features)

    if raw_count_matrix is not None:
        print("\nUsing CountVectorizer with raw data")
        run_clustering_algorithm(algorithm, test_data, raw_count_matrix, features)

    if entity_count_matrix is not None:
        print("\nUsing CountVectorizer with entities")
        run_clustering_algorithm(algorithm, test_data, entity_count_matrix, features)

    if token_count_matrix is not None:
        print("\nUsing CountVectorizer with tokens")
        run_clustering_algorithm(algorithm, test_data, token_count_matrix, features)

    if tfidf_matrix is not None:
        print("\nUsing TfidfVectorizer")
        run_clustering_algorithm(algorithm, test_data, tfidf_matrix, features)


def run_clustering_algorithm(
    algorithm, test_data, tfidf_matrix, features, show_details=False
):
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

    # The following scores have to be considered with a grain of salt, since the author of
    # this incredible beautiful code doesn't fully understand it yet...
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
