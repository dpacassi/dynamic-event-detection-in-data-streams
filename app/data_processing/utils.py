import collections
import pymysql
import pandas
import spacy
import time
import re
import os
from warnings import simplefilter

from scipy.sparse import find
from sklearn.metrics import (
    completeness_score,
    homogeneity_score,
    v_measure_score,
    adjusted_rand_score,
    adjusted_mutual_info_score,
    silhouette_score,
)
from sklearn.metrics.cluster import normalized_mutual_info_score
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# Ignore all future warnings.
simplefilter(action="ignore", category=FutureWarning)


class Result:
    def __init__(
        self,
        title,
        labels,
        processing_time,
        features=None,
        vectorizer=None,
        tokenizer=None,
        parameters=None,
    ):
        self.title = title
        self.labels = labels
        self.features = features
        self.parameters = parameters
        self.vectorizer = vectorizer
        self.tokenizer = tokenizer
        self.processing_time = processing_time

    def create_evaluation(self, y_true):
        # Number of clusters in labels, ignoring noise if present.
        return {
            "n_clusters": len(set(self.labels)) - (1 if -1 in self.labels else 0),
            "n_noise": list(self.labels).count(-1),
            "homogeneity_score": homogeneity_score(y_true, self.labels),
            "completeness_score": completeness_score(y_true, self.labels),
            "v_measure_score": v_measure_score(y_true, self.labels),
            "normalized_mutual_info_score": normalized_mutual_info_score(
                y_true, self.labels, average_method="arithmetic"
            ),
            "adjusted_rand_score": adjusted_rand_score(y_true, self.labels),
            "adjusted_mutual_info_score": adjusted_mutual_info_score(
                y_true, self.labels
            ),
        }

    def print_evaluation(self, y_true):
        scores = self.create_evaluation(y_true)
        print("------------------------------")
        print(self.title)
        print()
        print("Estimated number of clusters: %d" % scores["n_clusters"])
        print("Estimated number of noise points: %d" % scores["n_noise"])
        print("Homogeneity: %0.3f" % scores["homogeneity_score"])
        print("Completeness: %0.3f" % scores["completeness_score"])
        print("V-measure: %0.3f" % scores["v_measure_score"])
        print("NMI score: %0.3f" % scores["normalized_mutual_info_score"])
        print("Adjusted Rand Index: %0.3f" % scores["adjusted_rand_score"])
        print(
            "Adjusted Mutual Information: %0.3f" % scores["adjusted_mutual_info_score"]
        )
        print("Processing time: %0.2f seconds" % self.processing_time)
        print()

    def write_evaluation_to_db(self, y_true, db_id, time_total, real_clusters):
        scores = self.create_evaluation(y_true)
        connection = pymysql.connect(
            host=os.environ["MYSQL_HOSTNAME"],
            port=int(os.environ["MYSQL_PORT"]),
            user=os.environ["MYSQL_USER"],
            passwd=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        update_sql = "UPDATE cron_evaluation SET normalized_mutual_info_score = %s, adjusted_mutual_info_score = %s, completeness_score = %s, estimated_clusters = %s, real_clusters = %s, n_noise = %s, time_clustering = %s, time_total = %s, processed=1 WHERE id = %s"

        with connection.cursor() as cursor:
            s1 = float("{0:.8f}".format(scores['normalized_mutual_info_score']))
            s2 = float("{0:.8f}".format(scores['adjusted_mutual_info_score']))
            s3 = float("{0:.8f}".format(scores['completeness_score']))

            cursor.execute(update_sql, (s1, s2, s3, scores['n_clusters'], real_clusters, scores['n_noise'], self.processing_time, time_total, db_id))
            connection.commit()

        connection.close()


def remove_html(text):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, " ", text)

    return cleantext


def replace_non_alpha(text):
    text = re.sub("[^a-zA-Z]+", " ", text)

    return text


def replace_page_breaks(text):
    return re.sub(r"(\\n)", r"", text)


def remove_punctuation(text):
    cleaned = re.sub(r"[?|!|\'|#]", r"", text)
    cleaned = re.sub(r"[.|,|)|(|\|/]", r" ", cleaned)

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

    text = " ".join(filtered_words)

    return text


def stem_text(text, remove_stopwords=True):
    stop = stopwords.words("english")
    sno = SnowballStemmer("english")
    sentences = text.split(".")
    stemmed_text = []

    for sentence in sentences:
        sentence = sentence.strip()

        for word in sentence.split():
            if remove_stopwords and word not in stop:
                stemmed_text.append(sno.stem(word))
            elif not remove_stopwords:
                stemmed_text.append(sno.stem(word))

    text = " ".join(stemmed_text)

    return text


def lemmatize_text(text, remove_stopwords=True):
    stop = stopwords.words("english")
    nlp = spacy.load("en", disable=["parser", "ner"])
    sentences = text.split(".")
    lemmatized_text = []

    for sentence in sentences:
        sentence = sentence.strip()
        doc = nlp(sentence)

        if remove_stopwords:
            lemmatized_sentence = " ".join(
                [
                    token.lemma_
                    if token.lemma_ != "-PRON-" and token.lemma_ not in stop
                    else token.lower_
                    for token in doc
                ]
            )
        else:
            lemmatized_sentence = " ".join(
                [
                    token.lemma_ if token.lemma_ != "-PRON-" else token.lower_
                    for token in doc
                ]
            )

        lemmatized_text.append(lemmatized_sentence)

    text = ".".join(lemmatized_text)

    return text


def remove_common_words(text):
    common_words = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
        "year",
        "years",
        "month",
        "months",
        "day",
        "days",
        "hour",
        "hours",
        "minutes",
        "minute",
        "seconds",
        "second",
        "time",
        "date",
        "all",
        "rights",
        "reserved",
        "story",
        "reuters",
        "first",
        "second",
        "third",
        "soon",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "today",
        "now",
    ]
    doc = []

    for word in text.split():
        if word not in common_words:
            doc.append(word)

    text = " ".join(doc)

    return text


def clean_text(text, keep_stopwords=False, use_stemming=False, use_lemmatization=False):
    remove_stopwords = not keep_stopwords

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

    # Remove short words.
    text = remove_short_words(text)

    return text


def write_failed_to_db(db_id):
    if db_id > 0:
        connection = pymysql.connect(
            host=os.environ["MYSQL_HOSTNAME"],
            port=int(os.environ["MYSQL_PORT"]),
            user=os.environ["MYSQL_USER"],
            passwd=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        update_sql = "UPDATE cron_evaluation SET failed = 1 WHERE id = %s"

        with connection.cursor() as cursor:
            cursor.execute(update_sql, db_id)
            connection.commit()

        connection.close()


def write_preprocessing_time_to_db(db_id, preprocessing_time):
    if db_id > 0:
        connection = pymysql.connect(
            host=os.environ["MYSQL_HOSTNAME"],
            port=int(os.environ["MYSQL_PORT"]),
            user=os.environ["MYSQL_USER"],
            passwd=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        update_sql = "UPDATE cron_evaluation SET time_preprocessing = %s WHERE id = %s"

        with connection.cursor() as cursor:
            cursor.execute(update_sql, (preprocessing_time, db_id))
            connection.commit()

        connection.close()


def load_test_data(
    nrows=1000,
    skip_rows=0,
    skip_text_preprocessing=False,
    keep_stopwords=False,
    use_stemming=False,
    use_lemmatization=False,
    db_id=0,
):
    filepath = "test_data/clean_news_less_noisy.csv"

    names = [
        "id",
        "title",
        "url",
        "publisher",
        "category",
        "story",
        "hostname",
        "date",
        "newspaper_processed",
        "newspaper_meta_language",
        "newspaper_keywords",
        "newspaper_text",
    ]
    test_data = pandas.read_csv(
        filepath, nrows=nrows, skiprows=skip_rows, header=None, names=names
    )

    if not skip_text_preprocessing:
        start = time.time()
        test_data["newspaper_text"] = test_data["newspaper_text"].apply(
            clean_text, args=(keep_stopwords, use_stemming, use_lemmatization)
        )
        end = time.time()
        write_preprocessing_time_to_db(db_id, (end - start))
    else:
        write_preprocessing_time_to_db(db_id, 0)

    return test_data[test_data["newspaper_text"].notnull()]


def load_test_data_from_db(
    nrows=1000,
    skip_rows=0,
    skip_text_preprocessing=False,
    keep_stopwords=False,
    use_stemming=False,
    use_lemmatization=False,
    db_id=0,
):
    connection = pymysql.connect(
        host=os.environ["MYSQL_HOSTNAME"],
        port=int(os.environ["MYSQL_PORT"]),
        user=os.environ["MYSQL_USER"],
        passwd=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
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
        " LIMIT %s, %s"
    )

    data = pandas.read_sql(
        sql=get_sql, con=connection, index_col="id", params=[skip_rows, nrows]
    )
    connection.close()

    if not skip_text_preprocessing:
        start = time.time()
        data["newspaper_text"] = data["newspaper_text"].apply(
            clean_text, args=(keep_stopwords, use_stemming, use_lemmatization)
        )
        end = time.time()
        write_preprocessing_time_to_db(db_id, (end - start))
    else:
        write_preprocessing_time_to_db(db_id, 0)

    return data


def write_evaluation_result_in_db(
    method,
    sample_size,
    vectorizer,
    tokenizer,
    parameters,
    normalized_mutual_info_score,
    adjusted_mutual_info_score,
    completeness_score,
    estimated_clusters,
    real_clusters,
    n_noise,
    processing_time,
):

    connection = pymysql.connect(
        host=os.environ["MYSQL_HOSTNAME"],
        port=int(os.environ["MYSQL_PORT"]),
        user=os.environ["MYSQL_USER"],
        passwd=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    insert_sql = (
        "INSERT INTO method_evaluation"
        " (method, sample_size, vectorizer, tokenizer, parameters, normalized_mutual_info_score, adjusted_mutual_info_score, completeness_score, estimated_clusters, real_clusters, n_noise, processing_time)"
        " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    with connection.cursor() as cursor:
        cursor.execute(
            insert_sql,
            args=[
                method,
                sample_size,
                vectorizer,
                tokenizer,
                parameters,
                normalized_mutual_info_score,
                adjusted_mutual_info_score,
                completeness_score,
                estimated_clusters,
                real_clusters,
                n_noise,
                processing_time,
            ],
        )

    return connection.commit()


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
