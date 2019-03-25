import spacy
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    CountVectorizer,
    HashingVectorizer,
)


# The model has to be downloaded first!
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")


def get_tfidf_matrix(data, tokenizer=None):
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.HashingVectorizer.html 
    vectorizer = TfidfVectorizer(
        analyzer="word", max_features=1000, stop_words="english", tokenizer=tokenizer
    )
    matrix = vectorizer.fit_transform(data)
    features = vectorizer.get_feature_names()

    return matrix, features


def get_hash_matrix(data, tokenizer=None):
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.HashingVectorizer.html
    vectorizer = HashingVectorizer(
        analyzer="word", stop_words="english", tokenizer=tokenizer
    )
    matrix = vectorizer.fit_transform(data)

    return matrix, []


def get_count_matrix(data, tokenizer=None):
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
    vectorizer = CountVectorizer(
        analyzer="word", stop_words="english", tokenizer=tokenizer
    )
    matrix = vectorizer.fit_transform(data)
    features = vectorizer.get_feature_names()

    return matrix, features


def extract_entities(data):
    # https://spacy.io/usage/linguistic-features#named-entities
    doc = nlp(data)
    entities = [entity.text for entity in doc.ents]
    if len(entities) == 0:
        entities = ['empty']

    return entities


def extract_tokens(data):
    # https://spacy.io/usage/linguistic-features#tokenization
    doc = nlp(data)
    return [token.text for token in doc]