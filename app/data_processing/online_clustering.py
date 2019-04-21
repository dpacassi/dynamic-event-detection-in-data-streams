import db
import os
import utils
import argparse
import time
import difflib
import sys

from pprint import pprint
from dotenv import load_dotenv
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from deepdiff import DeepDiff

script_name = os.path.basename(__file__)


def cluster_news_by_date(nrows, date=None):
    if date is None:
        last_script_execution = db.get_last_script_execution(script_name)
        date = last_script_execution["last_processed_date"].values[0] if last_script_execution is not None else None
    news_articles = db.get_news_articles_from_date(date, nrows)
    return cluster_news(news_articles)


def cluster_news_by_nrows(nrows):
    news_articles = db.get_news_articles(nrows)
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
    return convert_labels_to_cluster_identifier(labels, list(news_articles.index.values)), news_articles["date"].values[0]


def convert_labels_to_cluster_identifier(labels, news_ids):
    grouped_indices = utils.group_data_by_label(labels)
    clusters = set()

    for key, indicies in grouped_indices.items():
        ids = [news_ids[index] for index in indicies]
        ids.sort()
        clusters.add(','.join(map(str,ids)))

    return clusters


# The online method works by regularly fetching articles from a certain date
# and cluster them. Once in a while the whole (limited by nrows) dataset will be clustered again.
# After each clustering step, the result is compared with the previous one
# to recognise new clusters or changes in existing clusters.

load_dotenv()

ap = argparse.ArgumentParser()
ap.add_argument("--full-cluster", dest="full_cluster", action="store_true")
ap.add_argument("--rows", required=False, type=int, default=1000)
ap.add_argument("--date", required=False, type=str, default=None)

ap.set_defaults(full_cluster=False)

args = vars(ap.parse_args())

log_message = ""
failed = False
last_processed_date = "0000-00-00 00:00:00"

start = time.time()

try:
    if args["full_cluster"]:
        clusters, last_processed_date = cluster_news_by_nrows(args["rows"])
    else:
        clusters, last_processed_date = cluster_news_by_date(args["rows"], args["date"])

    existing_clusters = db.get_clusters()

    if len(existing_clusters) > 0:
        existing_clusters = set(existing_clusters['identifier'].values.tolist())
        difference = clusters - existing_clusters
    else:
        difference = clusters

    print("----------------------")
    print("Differences")
    print(difference)
    print("New: {}".format(len(clusters)))
    print("Existing: {}".format(len(existing_clusters)))
    print("Number of differences: {}".format(len(difference)))
    print("Diff:")

    # convert to list to create the diff
    existing_clusters = list(existing_clusters)
    clusters = list(clusters)
    existing_clusters.sort()
    clusters.sort()

    differ = difflib.Differ()
    result = list(differ.compare(existing_clusters, clusters))
    # pprint(result)

    # Write diff into file
    htmldiff = difflib.HtmlDiff()
    html = htmldiff.make_file(existing_clusters, clusters, fromdesc='existing_clusters', todesc='clusters')
    myfile = open("diff.html", 'w')
    myfile.write(html)
    myfile.close()

    print("DeepDiff:")
    existing_clusters_list = [identifier.split(',') for identifier in existing_clusters]
    clusters_list = [identifier.split(',') for identifier in clusters]
    ddiff = DeepDiff(existing_clusters_list, clusters_list, ignore_order=True)
    pprint(ddiff['iterable_item_added'])

    print("----------------------")

    for cluster in difference:
        db.add_cluster(cluster)

except BaseException as err:
    failed = True
    log_message = str(err)

end = time.time()
processing_time = end - start
db.add_script_execution(script_name, str(last_processed_date), failed, log_message, processing_time)

# Test run:
# Start with partial clusters: 
# * python data_processing/online_clustering.py --date "2014-03-11 00:00:00"
# * python data_processing/online_clustering.py --date "2014-03-12 00:00:00"
# * python data_processing/online_clustering.py --date "2014-03-12 12:00:00"
# * python data_processing/online_clustering.py --date "2014-03-12 14:00:00"
# * python data_processing/online_clustering.py --date "2014-03-13 12:00:00"
# * python data_processing/online_clustering.py --date "2014-03-13 13:00:00"
# Finally do a full cluster:  
# * python data_processing/online_clustering.py --rows 5000


# ToDos:
# Detect type of change:
# * addition
# * change
# * deletion
# Add most important keyterms to name a cluster