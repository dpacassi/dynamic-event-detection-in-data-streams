import db
import os
import utils
import argparse
import time

from dotenv import load_dotenv
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from datasketch import MinHash, MinHashLSH

script_name = os.path.basename(__file__)


class Event:
    TOPIC_ADDED = 1
    TOPIC_CHANGED = 2
    TOPIC_DELETED = 3


def cluster_news_by_date(nrows, date=None):
    if date is None:
        last_script_execution = db.get_last_script_execution(script_name)
        date = (
            last_script_execution["last_processed_date"].values[0]
            if last_script_execution is not None
            else None
        )
    news_articles = db.get_news_articles_from_date(date, nrows)
    return cluster_news(news_articles)


def cluster_news_by_nrows(nrows):
    news_articles = db.get_news_articles(nrows)
    return cluster_news(news_articles)


def cluster_news(news_articles):
    vectorizer = TfidfVectorizer(
        min_df=3, max_df=0.9, lowercase=True, analyzer="word", stop_words="english"
    )

    model = HDBSCAN(min_cluster_size=5, metric="cosine")

    data_matrix = vectorizer.fit_transform(news_articles["newspaper_text"])
    labels = model.fit_predict(data_matrix)

    # Clusters are identified by a sorted string of news ids
    return (
        convert_labels_to_cluster_identifier(labels, list(news_articles.index.values)),
        news_articles["date"].values[0],
    )


def convert_labels_to_cluster_identifier(labels, news_ids):
    grouped_indices = utils.group_data_by_label(labels)
    clusters = set()

    for key, indicies in grouped_indices.items():
        ids = [news_ids[index] for index in indicies]
        ids.sort()
        clusters.add(",".join(map(str, ids)))

    return clusters


def find_changes_in_clusters(existing_clusters, new_cluster_identifiers):
    changed_clusters = []
    unchanged_clusters = []
    new_clusters = []

    lsh = MinHashLSH(threshold=0.9, num_perm=128)

    for index, cluster in existing_clusters.iterrows():
        m = create_minhash(cluster["identifier"])
        lsh.insert(index, m)

    for identifier in new_cluster_identifiers:
        m = create_minhash(identifier)
        cluster_ids = lsh.query(m)

        if len(cluster_ids) == 0:
            new_clusters.append(identifier)
        else:
            cluster_id = int(cluster_ids[0])
            existing_identifier = existing_clusters.loc[cluster_id]["identifier"]
            existing_news = set(existing_identifier.split(","))
            new_news = set(identifier.split(","))

            additions = new_news - existing_news
            deletions = existing_news - new_news

            if len(additions) == 0 and len(deletions) == 0:
                unchanged_clusters.append(identifier)
            else:
                changed_clusters.append(
                    {
                        "cluster_id": cluster_id,
                        "old_identifier": existing_identifier,
                        "new_identifier": identifier,
                        "additions": additions,
                        "deletions": deletions,
                    }
                )

    return changed_clusters, unchanged_clusters, new_clusters


def create_minhash(identifier):
    m = MinHash(num_perm=128)
    for d in set(identifier.split(",")):
        m.update(d.encode("utf8"))

    return m


def run(date, rows, full_cluster=False, verbose=False):
    # The online method works by regularly fetching articles from a certain date
    # and cluster them. Once in a while the whole (limited by nrows) dataset will be clustered again.
    # After each clustering step, the result is compared with the previous one
    # to recognise new clusters or changes in existing clusters.

    load_dotenv()

    log_message = ""
    failed = False
    last_processed_date = "0000-00-00 00:00:00"

    start = time.time()

    try:
        clusters, last_processed_date = cluster_news_by_date(rows, date)
        existing_clusters = db.get_clusters()
        changed_clusters, unchanged_clusters, new_clusters = find_changes_in_clusters(
            existing_clusters, clusters
        )

        # Add new clusters
        for cluster in new_clusters:
            cluster_id = db.add_cluster(cluster)
            db.add_event(Event.TOPIC_ADDED, cluster_id)

        # Process changed clusters
        for cluster in changed_clusters:
            cluster_id = cluster["cluster_id"]
            changes = {}

            if full_cluster:
                identifier = cluster["new_identifier"]
                changes["additions"] = cluster["additions"]
                changes["deletions"] = cluster["deletions"]
            else:
                # In partial clusters deletions will be ignored, since the deleted articles are most likely not part of
                # the sample subset. We could check in the future if deleted articles are part of the current subset.
                changes["additions"] = cluster["additions"]
                identifier = cluster["new_identifier"].split(",")
                identifier += cluster["additions"]
                identifier.sort()
                identifier = ",".join(identifier)

            db.update_cluster(cluster_id, identifier)
            if (
                "additions" in changes
                and len(changes["additions"]) > 0
                or "deletions" in changes
                and len(changes["deletions"]) > 0
            ):
                db.add_event(Event.TOPIC_CHANGED, cluster_id, str(changes))

        if verbose:
            print("----------------------")
            print("Changed clusters:")
            print(changed_clusters)
            print("Unchanged clusters:")
            print(unchanged_clusters)
            print("New clusters:")
            print(new_clusters)
            print("----------------------")
            print("Statistics:")
            print("Number of changed clusters:", len(changed_clusters))
            print("Number of unchanged clusters:", len(unchanged_clusters))
            print("Number of new clusters:", len(new_clusters))
            print("----------------------")

    except ArithmeticError as err:
        if verbose:
            print("----------------------")
            print("Error:")
            print(err)

        failed = True
        log_message = str(err)

    end = time.time()
    processing_time = end - start
    db.add_script_execution(
        script_name, str(last_processed_date), failed, log_message, processing_time
    )


# Test run:
# Start with partial clusters:
# * python data_processing/online_clustering.py --date "2014-03-11 00:00:00"
# * python data_processing/online_clustering.py --date "2014-03-11 12:00:00"
# * python data_processing/online_clustering.py --date "2014-03-12 12:00:00" --rows 2000
# * python data_processing/online_clustering.py --date "2014-03-12 13:00:00" --rows 2000
# * python data_processing/online_clustering.py --date "2014-03-13 12:00:00"
# * python data_processing/online_clustering.py --date "2014-03-13 13:00:00"
# Finally do a full cluster:
# * python data_processing/online_clustering.py --rows 5000

# ToDos:
# Detect type of change:
# * Topic addition
# * Topic change
# * Topic deletion
# Add most important keyterms to name a cluster
#
# Considerations:
# * Consider deletions only on full clusterings, otherwise the article was simply not part of the sample size.


if __name__ == "__main__":
    load_dotenv()

    ap = argparse.ArgumentParser()
    ap.add_argument("--full-cluster", dest="full_cluster", action="store_true")
    ap.add_argument("--verbose", dest="verbose", action="store_true")
    ap.add_argument("--rows", required=False, type=int, default=1000)
    ap.add_argument("--date", required=False, type=str, default=None)
    ap.set_defaults(full_cluster=False)
    ap.set_defaults(verbose=False)
    args = vars(ap.parse_args())

    full_cluster = args["full_cluster"]
    rows = args["rows"]
    date = args["date"]
    verbose = args["verbose"]

    run(date, rows, full_cluster, verbose)
