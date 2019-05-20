import db
import os
import utils
import argparse
import time
import collections
from itertools import chain
from dotenv import load_dotenv
from hdbscan import HDBSCAN, approximate_predict
from sklearn.feature_extraction.text import TfidfVectorizer
from datasketch import MinHash, MinHashLSH
from datetime import datetime
from datetime import timedelta

script_name = os.path.basename(__file__)

# The model is global, since we need the same instance for each batch
model = HDBSCAN(min_cluster_size=5, metric="euclidean", prediction_data=True)
vectorizer = TfidfVectorizer(min_df=3, max_df=0.9, lowercase=True, max_features=50000, analyzer="word", stop_words="english")


def predict_news_cluster_by_date(nrows, date):
    last_script_execution = db.get_last_script_execution(script_name)
    last_processed_date = (
        last_script_execution["last_processed_date"].values[0]
        if last_script_execution is not None
        else None
    )

    # Load only news articles since the last batch
    news_articles = db.get_news_articles_from_startdate_to_enddate(str(last_processed_date), str(date), nrows)
    data_matrix = vectorizer.transform(news_articles["text_lemmatized_without_stopwords"])
    labels, probabilities = approximate_predict(model, data_matrix.toarray())

    # Clusters are identified by a sorted string of news ids
    return labels
