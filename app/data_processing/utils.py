import collections
import pymysql
import pandas
import time
import re
import os
from warnings import simplefilter

from scipy.sparse import find

# Ignore all future warnings.
simplefilter(action="ignore", category=FutureWarning)


def get_labels_and_documents_from_distribution_matrix(
    document_matrix, test_data, threshold=0.7
):
    documents_by_topic = collections.defaultdict(list)
    labels = []

    for row, document in enumerate(document_matrix):
        max_topic_distribution_value = 0
        max_topic_distribution_index = 0
        for index, topic_distribution in enumerate(document):
            if topic_distribution > max_topic_distribution_value:
                max_topic_distribution_value = topic_distribution
                max_topic_distribution_index = index

        if max_topic_distribution_value < threshold:
            max_topic_distribution_index = -1

        documents_by_topic[max_topic_distribution_index].append(
            [max_topic_distribution_value, test_data.iloc[row]]
        )
        labels.append(max_topic_distribution_index)

    return labels, documents_by_topic


def map_features_to_word_vectors(data_matrix, features):
    features_by_document = []
    for sparse_row in data_matrix:
        row_indices, column_indices, values = find(sparse_row)
        features_by_document.append([features[index] for index in column_indices])
    return features_by_document


def group_data_by_label(labels):
    grouped_indices = collections.defaultdict(list)
    for index, value in enumerate(labels):
        if value >= 0:
            grouped_indices[value].append(index)
    return grouped_indices


def convert_labels_to_cluster_identifier(labels, news_ids):
    grouped_indices = group_data_by_label(labels)
    clusters = set()

    for key, indicies in grouped_indices.items():
        ids = [news_ids[index] for index in indicies]
        ids.sort()
        clusters.add(",".join(map(str, ids)))

    return clusters
