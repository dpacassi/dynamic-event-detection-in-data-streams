import collections
import pandas
import re

from sklearn.metrics import accuracy_score, completeness_score
from sklearn.metrics.cluster import normalized_mutual_info_score
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

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


def remove_html(text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', text)

    return cleantext


def replace_non_alpha(text):
    text = re.sub('[^a-zA-Z]+', ' ', text)

    return text


def remove_punctuation(text):
    cleaned = re.sub(r'[?|!|\'|#]', r'', text)
    cleaned = re.sub(r'[.|,|)|(|\|/]', r' ', cleaned)

    return cleaned


def remove_multiple_whitespaces(text):
    " ".join(text.split())

    return text


def remove_short_words(text):
    filtered_words = []

    for word in text.split():
        if len(word) > 2:
            filtered_words.append(word)
        else:
            continue

    text = ' '.join(filtered_words)

    return text


def stem_text(text):
    stop = stopwords.words('english')
    sno = SnowballStemmer('english')
    stemmed_words = []

    for word in text.split():
        if word not in stop:
            stemmed_words.append(sno.stem(word))

    text = ' '.join(stemmed_words)

    return text


def clean_text(text):
    # Trim text.
    text = text.strip()

    # Transform the text to lower case.
    text = text.lower()

    # Remove any existing HTML tags.
    text = remove_html(text)

    # Replace all non alphabetical characters with spaces.
    text = replace_non_alpha(text)

    # Remove punctuation.
    # Obsolete since we remove all non alphabetical characters.
    #text = remove_punctuation(text)

    # Remove multiple whitespaces.
    text = remove_multiple_whitespaces(text)

    # Remove single characters.
    text = remove_short_words(text)

    # Text stemming and stop words removal.
    text = stem_text(text)

    return text


def load_test_data(content_column="newspaper_text", nrows=None):
    # filepath = "test_data/uci-news-aggregator.csv"
    # filepath = "test_data/export.csv"
    filepath = "test_data/clean_news.csv"

    test_data = pandas.read_csv(filepath, nrows=nrows)
    test_data[content_column] = test_data[content_column].apply(clean_text)

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
