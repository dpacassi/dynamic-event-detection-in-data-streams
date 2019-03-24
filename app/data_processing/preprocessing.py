import spacy
from sklearn.feature_extraction.text import TfidfVectorizer


def get_tfidf_matrix(data):
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', max_features=1000, stop_words='english')
    matrix = tfidf_vectorizer.fit_transform(data)
    features = tfidf_vectorizer.get_feature_names()

    return matrix, features


def extract_entities(data):
    # nlp = init_spacy()
    raise NotImplementedError()


def extract_keywords(data):
    raise NotImplementedError()


def init_spacy():
    return spacy.load("en")
