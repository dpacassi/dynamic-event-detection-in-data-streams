from sklearn.feature_extraction.text import TfidfVectorizer
corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?',
]

corpus = [
    'Hello',
    'Hello',
    'Hello',
    'World',
    'Held',
    'Hello World'
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

# print(vectorizer.get_feature_names())
# print(X.shape)

print(X)
