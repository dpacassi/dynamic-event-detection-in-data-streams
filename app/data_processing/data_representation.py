from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from tabulate import tabulate
from scipy import spatial
import numpy as np

corpus = [
    'Rosetta space probe scopes out landing zone',
    'Landing site search for Rosetta narrows',
    'Major Bank Shake-up At Bank of England'
]

# Tfidf.
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(corpus)
f_names = vectorizer.get_feature_names()
table = []

for i, row in enumerate(X):
    dense_row = np.squeeze(np.asarray(row.todense()))
    table.append(dense_row)

latex = tabulate(table, headers=f_names, tablefmt="latex", floatfmt=".3f")
# print(latex)

# Similarity.
s_table = []
for i, row in enumerate(X):
    dense_row = np.squeeze(np.asarray(row.todense()))
    s = dense_row.tolist()
    s_table.append(s)

result = 1 - spatial.distance.cosine(s_table[0], s_table[1])
print(result)

result = 1 - spatial.distance.cosine(s_table[1], s_table[2])
print(result)

# Count.
vectorizer = CountVectorizer(stop_words="english")
X = vectorizer.fit_transform(corpus)
f_names = vectorizer.get_feature_names()
table = []

for i, row in enumerate(X):
    dense_row = np.squeeze(np.asarray(row.todense()))
    table.append(dense_row)

latex = tabulate(table, headers=f_names, tablefmt="latex", floatfmt=".3f")
# print(latex)