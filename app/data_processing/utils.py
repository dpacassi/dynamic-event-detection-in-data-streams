import collections
import pandas
import spacy
import re
import os
import pymysql

from scipy.sparse import find
from sklearn.metrics import accuracy_score, completeness_score, precision_recall_fscore_support
from sklearn.metrics.cluster import normalized_mutual_info_score
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


class Result:
    def __init__(self, title, labels, n_topics, processing_time, features=None):
        self.title = title
        self.labels = labels
        self.n_topics = n_topics
        self.features = features
        self.processing_time = processing_time

    def print_evaluation(self, y_true):
        print("------------------------------")
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
        print("Accuracy: %0.3f" % accuracy_score(y_true, self.labels))
        precision, recall, fscore, support = precision_recall_fscore_support(y_true, self.labels, average='micro')
        # print("Precision: %0.3f" % precision)
        # print("Recall: %0.3f" % recall)
        print("F-score: %0.3f" % fscore)
        print("Processing time: %0.2f seconds" % self.processing_time)
        print()


def remove_html(text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', text)

    return cleantext


def replace_non_alpha(text):
    text = re.sub('[^a-zA-Z]+', ' ', text)

    return text


def replace_page_breaks(text):
    return re.sub(r'(\\n)', r'', text)


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


def stem_text(text, remove_stopwords=True):
    stop = stopwords.words('english')
    sno = SnowballStemmer('english')
    sentences = text.split('.')
    stemmed_text = []

    for sentence in sentences:
        sentence = sentence.strip()

        for word in sentence.split():
            if remove_stopwords and word not in stop:
                stemmed_text.append(sno.stem(word))
            elif not remove_stopwords:
                stemmed_text.append(sno.stem(word))

    text = ' '.join(stemmed_text)

    return text


def lemmatize_text(text, remove_stopwords=True):
    stop = stopwords.words('english')
    nlp = spacy.load('en', disable=['parser', 'ner'])
    sentences = text.split('.')
    lemmatized_text = []

    for sentence in sentences:
        sentence = sentence.strip()
        doc = nlp(sentence)

        if remove_stopwords:
            lemmatized_sentence = ' '.join([token.lemma_ if token.lemma_ != '-PRON-' and token.lemma_ not in stop else token.lower_ for token in doc])
        else:
            lemmatized_sentence = ' '.join([token.lemma_ if token.lemma_ != '-PRON-' else token.lower_ for token in doc])

        lemmatized_text.append(lemmatized_sentence)

    text = '.'.join(lemmatized_text)

    return text


def remove_common_words(text):
  common_words = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'year', 'years', 'month', 'months', 'day', 'days', 'hour', 'hours', 'minutes', 'minute', 'seconds', 'second', 'time', 'date', 'all', 'rights', 'reserved', 'story', 'reuters', 'first', 'second', 'third', 'soon', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'today', 'now']
  doc = []

  for word in text.split():
      if word not in common_words:
          doc.append(word)

  text = ' '.join(doc)

  return text


def clean_text(text, remove_stopwords=True, use_stemming=False, use_lemmatization=False):
    # Trim text.
    text = text.strip()

    # Transform the text to lower case.
    text = text.lower()

    # Remove page breaks
    text = replace_page_breaks(text)

    # Remove any existing HTML tags.
    text = remove_html(text)

    # Remove common words.
    text = remove_common_words(text)

    # Text lemmatization with spaCy.
    if use_lemmatization:
        text = lemmatize_text(text, remove_stopwords)

    # Text stemming.
    if use_stemming:
        text = stem_text(text, remove_stopwords)

    # Replace all non alphabetical characters with spaces.
    text = replace_non_alpha(text)

    # Remove punctuation.
    # Obsolete since we remove all non alphabetical characters.
    # text = remove_punctuation(text)

    # Remove multiple whitespaces.
    text = remove_multiple_whitespaces(text)

    # Remove single characters.
    text = remove_short_words(text)

    return text


def load_test_data(content_column="newspaper_text", nrows=None, skip_rows=0):
    # filepath = "test_data/uci-news-aggregator.csv"
    # filepath = "test_data/export.csv"
    filepath = "test_data/clean_news_less_noisy.csv"

    names = ['id', 'title', 'url', 'publisher', 'category', 'story', 'hostname', 'date', 'newspaper_processed', 'newspaper_meta_language', 'newspaper_keywords', 'newspaper_text']
    test_data = pandas.read_csv(filepath, nrows=nrows, skiprows=skip_rows, header=None, names=names)
    test_data[content_column] = test_data[content_column].apply(clean_text)

    return test_data[test_data[content_column].notnull()]


def load_test_data_from_db(nrows=1000, skip_rows=0):
    connection = pymysql.connect(
        host=os.environ['MYSQL_HOSTNAME'],
        port=int(os.environ['MYSQL_PORT']),
        user=os.environ['MYSQL_USER'],
        passwd=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    get_sql = (
        "SELECT *"
        " FROM news_article"
        " WHERE"
        "     newspaper_processed = 1"
        "     AND title_keywords_intersection = 1"
        "     AND hostname != 'newsledge.com'"
        "     AND hostname != 'www.newsledge.com'"
        "     AND newspaper_text IS NOT NULL"
        "     AND TRIM(COALESCE(newspaper_text, '')) != ''"
        "     AND newspaper_text NOT LIKE '%%GDPR%%'"
        "     AND newspaper_text NOT LIKE '%%javascript%%'"
        "     AND newspaper_text NOT LIKE '%%404%%'"
        "     AND newspaper_text NOT LIKE '%%cookie%%'"
        " ORDER BY id ASC"
        " LIMIT %s"
    )

    data = pandas.read_sql(sql=get_sql, con=connection, index_col='id', params=[nrows])
    connection.close()

    return data


def get_labels_and_documents_from_distribution_matrix(document_matrix, test_data, threshold=0.7):
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

        documents_by_topic[max_topic_distribution_index].append([max_topic_distribution_value, test_data.iloc[row]])
        labels.append(max_topic_distribution_index)

    return labels, documents_by_topic


def map_features_to_word_vectors(data_matrix, features):
    features_by_document = []
    for sparse_row in data_matrix:
        row_indices, column_indices, values = find(sparse_row)
        features_by_document.append([features[index] for index in column_indices])
    return features_by_document
