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
        min_df=2,
        max_df=0.8,
        lowercase=True,
        max_features=2000,
        analyzer="word",
        stop_words="english",
        tokenizer=tokenizer,
    )
    matrix = vectorizer.fit_transform(data)
    features = vectorizer.get_feature_names()

    return matrix, features


def get_hash_matrix(data, tokenizer=None):
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.HashingVectorizer.html
    vectorizer = HashingVectorizer(
        analyzer="word", stop_words="english", tokenizer=tokenizer, n_features=2 ** 18
    )
    matrix = vectorizer.fit_transform(data)

    return matrix, []


def get_count_matrix(data, tokenizer=None):
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
    vectorizer = CountVectorizer(
        min_df=2,
        max_df=0.8,
        token_pattern="[a-zA-Z\-][a-zA-Z\-]{2,}",
        lowercase=True,
        max_features=5000,
        analyzer="word",
        stop_words="english",
        tokenizer=tokenizer,
        ngram_range=(1, 2)
    )
    matrix = vectorizer.fit_transform(data)
    features = vectorizer.get_feature_names()

    return matrix, features


def lemmatize_word(data):
    # https://spacy.io/usage/linguistic-features#named-entities
    doc = nlp(data)
    return [token.lemma_ for token in doc]


def extract_entities(data):
    # https://spacy.io/usage/linguistic-features#named-entities
    doc = nlp(data)
    entities = [entity.text for entity in doc.ents]
    if len(entities) == 0:
        entities = ["empty"]

    return entities


def extract_tokens(data):
    # https://spacy.io/usage/linguistic-features#tokenization
    doc = nlp(data)
    return [token.text for token in doc]
