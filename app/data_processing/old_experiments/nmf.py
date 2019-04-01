from __future__ import print_function
from time import time

import pandas 
import collections

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.cluster import normalized_mutual_info_score, adjusted_mutual_info_score

from sklearn.preprocessing import LabelEncoder


n_samples = 2000
n_features = 1000
n_topics = 27
n_top_words = 20


t0 = time()
print("Loading dataset and extracting TF-IDF features...")


def load_test_data(nrows=None):
    # filepath = "test_data/uci-news-aggregator.csv"
    # filepath = "test_data/export.csv"
    filepath = "test_data/clean_news.csv"

    test_data = pandas.read_csv(filepath, nrows=nrows)
    return test_data


dataset = load_test_data()

vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                             stop_words='english')
tfidf = vectorizer.fit_transform(dataset['newspaper_text'])
print("done in %0.3fs." % (time() - t0))

# Fit the NMF model
print("Fitting the NMF model with n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

document_matrix = nmf.transform(tfidf)
print(nmf.transform(tfidf))

documents_by_topic = collections.defaultdict(list)
y_predict = []
for row, document in enumerate(document_matrix):
    max_topic_distribution_value = 0
    max_topic_distribution_index = 0
    for index, topic_distribution in enumerate(document):
        if topic_distribution > max_topic_distribution_value:
            max_topic_distribution_value = topic_distribution
            max_topic_distribution_index = index

    documents_by_topic[max_topic_distribution_index].append([max_topic_distribution_value, dataset.iloc[row]])
    y_predict.append(max_topic_distribution_index)

y_true = LabelEncoder().fit_transform(dataset['story'])
print(y_predict)

feature_names = vectorizer.get_feature_names()

for topic_idx, topic in enumerate(nmf.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


print("NMF score: %0.3f" % normalized_mutual_info_score(y_true, y_predict, average_method='arithmetic'))
