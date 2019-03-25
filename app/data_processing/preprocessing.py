import spacy
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    CountVectorizer,
    HashingVectorizer,
)


def get_tfidf_matrix(data):
    vectorizer = TfidfVectorizer(
        analyzer="word", max_features=1000, stop_words="english"
    )
    matrix = vectorizer.fit_transform(data)
    features = vectorizer.get_feature_names()

    return matrix, features


def get_hash_matrix(data):
    vectorizer = HashingVectorizer(
        analyzer="word", stop_words="english"
    )
    matrix = vectorizer.fit_transform(data)

    return matrix, []


def get_count_matrix(data):
    vectorizer = CountVectorizer(
        analyzer="word", stop_words="english"
    )
    matrix = vectorizer.fit_transform(data)
    features = vectorizer.get_feature_names()

    return matrix, features


def extract_entities(data):
    # nlp = init_spacy()
    raise NotImplementedError()


def extract_keywords(data):
    raise NotImplementedError()


def init_spacy():
    return spacy.load("en")
