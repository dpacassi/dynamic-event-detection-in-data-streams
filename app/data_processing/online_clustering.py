import db
import os
import utils
import argparse

from hdbscan import HDBSCAN
from sklearn.vectorizer import TfidfVectorizer

script_name = os.path.basename(__file__)


def cluster_news_by_date():
    last_script_execution = db.get_last_script_execution(script_name)
    last_execution_date = last_script_execution["execution_date"] if last_script_execution is not None else None
    news_articles = db.get_news_articles(last_execution_date)
    return cluster_news(news_articles)


def cluster_news_by_nrows(nrows=1000):
    news_articles = db.get_news_articles(None, nrows=1000)
    return cluster_news(news_articles)


def cluster_news(news_articles):
    vectorizer = TfidfVectorizer(
        min_df=3,
        max_df=0.9,
        lowercase=True,
        analyzer="word",
        stop_words="english",
    )

    model = HDBSCAN(
        min_cluster_size=5,
        metric="cosine",
    )

    data_matrix = vectorizer.fit_transform(news_articles["newspaper_text"])
    labels = model.fit_predict(data_matrix)

    # Clusters are identified by a sorted string of news ids
    return convert_labels_to_cluster_identifier(labels, news_articles["id"])


def convert_labels_to_cluster_identifier(labels, news_ids):
    grouped_indices = utils.group_data_by_label(labels)
    clusters = set()

    for indicies in grouped_indices:
        ids = [news_ids[index] for index in indicies]
        ids.sort()
        clusters.add(','.join(ids))

    return clusters


# The online method works by regularly fetching articles from a certain date
# and cluster them. Once in a while the whole (limited by nrows) dataset will be clustered again.
# After each clustering step, the result is compared with the previous one
# to recognise new clusters or changes in existing clusters.

ap = argparse.ArgumentParser()
ap.add_argument("--ignore-date", dest="ignore_date", action="store_true")
ap.add_argument("--rows", required=False, type=int, default=1000)


if argparse["ignore_date"]:
    clusters = cluster_news_by_nrows(argparse["nrows"])
else:
    clusters = cluster_news_by_date


existing_clusters = db.get_clusters()
difference = clusters - existing_clusters

print(difference)

db.add_script_execution(script_name)