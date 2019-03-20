import spacy
from sklearn.feature_extraction.text import TfidfVectorizer


def get_tfidf_matrix(data):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    return tfidf_vectorizer.fit_transform(data)


def extract_entities(data):
    # nlp = init_spacy()
    raise NotImplementedError()


def extract_keywords(data):
    raise NotImplementedError()


def init_spacy():
    return spacy.load("en")
