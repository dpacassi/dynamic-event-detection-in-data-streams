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
    apply_hdbscan,
    apply_optics,
    apply_meanshift,
    apply_affinity_propagation,
    apply_birch,
)


id_column = "id"
content_column = "newspaper_text"
story_column = "story"


def main():

    print("Load test data.")
    test_data = load_test_data(nrows=1000)

    print("Create data matrices.")
    text = test_data[content_column]

    # tfidf_matrix, features = get_tfidf_matrix(text)
    # count_matrix, features = get_count_matrix(text)

    raw_hash_matrix, features = get_hash_matrix(text)
    entity_hash_matrix, features = get_hash_matrix(text, extract_entities)
    # token_hash_matrix, features = get_hash_matrix(text, extract_tokens)

    print("Cluster data.")

    print("------------------------------")
    print("DBSCAN:")
    run_algorithm_with_different_vectorizers(
        apply_dbscan,
        test_data,
        features,
        count_matrix=None,
        raw_hash_matrix=raw_hash_matrix,
        entity_hash_matrix=entity_hash_matrix,
        token_hash_matrix=None,
        tfidf_matrix=None
    )

    print("------------------------------")
    print("HDBSCAN:")
    run_algorithm_with_different_vectorizers(
        apply_hdbscan,
        test_data,
        features,
        count_matrix=None,
        raw_hash_matrix=raw_hash_matrix,
        entity_hash_matrix=entity_hash_matrix,
        token_hash_matrix=None,
        tfidf_matrix=None
    )

    # print("------------------------------")
    # print("OPTICS:")
    # run_algorithm_with_different_vectorizer(
    #     apply_optics,
    #     test_data,
    #     features,
    #     None,
    #     None,
    #     None,
    #     token_hash_matrix.toarray(),
    #     None
    # )

    # print("------------------------------")
    # print("Affinity Propagation:")
    # run_clustering_algorithm(
    #     apply_affinity_propagation, test_data, tfidf_matrix, features
    # )

    # print("------------------------------")
    # print("Birch:")
    # run_clustering_algorithm(apply_birch, test_data, tfidf_matrix, features)

    # print('------------------------------')
    # print("Meanshift:")
    # run_clustering_algorithm(apply_meanshift, test_data, tfidf_matrix.todense(), features, False)


def run_algorithm_with_different_vectorizers(
    algorithm,
    test_data,
    features,
    count_matrix,
    raw_hash_matrix,
    entity_hash_matrix,
    token_hash_matrix,
    tfidf_matrix
):
    if count_matrix is not None:
        print("Using CountVectorizer")
        run_clustering_algorithm(algorithm, test_data, count_matrix, features)

    if raw_hash_matrix is not None:
        print("\nUsing HashVectorizer with raw data")
        run_clustering_algorithm(algorithm, test_data, raw_hash_matrix, features)

    if entity_hash_matrix is not None:
        print("\nUsing HashVectorizer with entities")
        run_clustering_algorithm(algorithm, test_data, entity_hash_matrix, features)

    if token_hash_matrix is not None:
        print("\nUsing HashVectorizer with tokens")
        run_clustering_algorithm(algorithm, test_data, token_hash_matrix, features)

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

    cluster_set = set(test_data[story_column])
    actual_clusters = len(cluster_set)

    cluster_dict = {}
    for index, cluster in enumerate(cluster_set):
        cluster_dict[cluster] = index

    labels_true = []
    for story in test_data[story_column].values:
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
                print(test_data[id_column][index])
                print(test_data[content_column][index])
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
    # filepath = "test_data/uci-news-aggregator.csv"
    # filepath = "test_data/export.csv"
    filepath = "test_data/clean_news.csv"

    test_data = pandas.read_csv(filepath, nrows=nrows)
    return test_data[test_data[content_column].notnull()]


if __name__ == "__main__":
    main()
