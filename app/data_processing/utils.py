import collections
import pandas

from sklearn.metrics import accuracy_score, completeness_score
from sklearn.metrics.cluster import normalized_mutual_info_score


class Result:
    def __init__(self, title, labels, n_topics):
        self.title = title
        self.labels = labels
        self.n_topics = n_topics

    def print_evaluation(self, y_true):
        print("--------------------------")
        print(self.title)
        print()
        print("Number of clusters: %d" % self.n_topics)
        print("Completeness: %0.3f" % completeness_score(y_true, self.labels))
        print(
            "NMI score: %0.3f"
            % normalized_mutual_info_score(
                y_true, self.labels, average_method="arithmetic"
            )
        )
        print()


def load_test_data(content_column="newspaper_text", nrows=None):
    # filepath = "test_data/uci-news-aggregator.csv"
    # filepath = "test_data/export.csv"
    filepath = "test_data/clean_news.csv"

    test_data = pandas.read_csv(filepath, nrows=nrows)
    return test_data[test_data[content_column].notnull()]


def get_labels_and_documents_from_distribution_matrix(document_matrix, test_data):
    documents_by_topic = collections.defaultdict(list)
    labels = []

    for row, document in enumerate(document_matrix):
        max_topic_distribution_value = 0
        max_topic_distribution_index = 0
        for index, topic_distribution in enumerate(document):
            if topic_distribution > max_topic_distribution_value:
                max_topic_distribution_value = topic_distribution
                max_topic_distribution_index = index

        documents_by_topic[max_topic_distribution_index].append([max_topic_distribution_value, test_data.iloc[row]])
        labels.append(max_topic_distribution_index)

    return labels, documents_by_topic
