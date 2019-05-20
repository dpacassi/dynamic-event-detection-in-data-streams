import db
import os
import utils
import argparse
import time
import collections
from itertools import chain
from dotenv import load_dotenv
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from datasketch import MinHash, MinHashLSH
from datetime import datetime
from datetime import timedelta

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

    #data_matrix = vectorizer.fit_transform(news_articles["newspaper_text"])
    data_matrix = vectorizer.fit_transform(news_articles["text_lemmatized_without_stopwords"])
    labels = model.fit_predict(data_matrix)

    # Clusters are identified by a sorted string of news ids
    return (
        utils.convert_labels_to_cluster_identifier(
            labels, list(news_articles.index.values)
        ),
        news_articles["computed_publish_date"].values[0],
    )


def find_changes_in_clusters(existing_clusters, new_cluster_identifiers):
    changed_clusters = []
    unchanged_clusters = []
    new_clusters = []

    lsh = MinHashLSH(threshold=0.75, num_perm=256)
    min_hashes = dict()
    for index, cluster in existing_clusters.iterrows():
        m = create_minhash(cluster["identifier"])
        min_hashes[index] = m
        lsh.insert(index, m)

    for identifier in new_cluster_identifiers:
        m = create_minhash(identifier)
        cluster_ids = lsh.query(m)

        if len(cluster_ids) == 0:
            new_clusters.append(identifier)
        else:
            cluster_id = find_best_match(m, min_hashes, cluster_ids)
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


def find_best_match(min_hash, min_hashes, cluster_ids):
    best_match = 0
    best_similarity = 0
    for cluster_id in cluster_ids:
        similarity = min_hash.jaccard(min_hashes[cluster_id])
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = cluster_id
    return best_match


def create_minhash(identifier):
    m = MinHash(num_perm=256)
    for d in set(identifier.split(",")):
        m.update(d.encode("utf8"))

    return m


def find_true_events(new_news_ids, existing_news_ids):
    new_stories = get_stories_from_news_ids(new_news_ids)
    existing_stories = get_stories_from_news_ids(existing_news_ids)

    addition_events = len(new_stories.keys() - existing_stories.keys())
    deletion_events = len(existing_stories.keys() - new_stories.keys())

    change_events = []

    if len(existing_stories) > 0:
        for story, news_ids in new_stories.items():
            existing_ids = existing_stories[story]
            additions = news_ids - existing_ids
            deletions = existing_ids - news_ids
            if len(additions) > 0 or len(deletions) > 0:
                change_events.append(
                    {"story": story, "additions": additions, "deletions": deletions}
                )

    return change_events, addition_events, deletion_events


def get_stories_from_news_ids(news_ids):
    if len(news_ids) == 0:
        return dict()

    news = db.load_news_by_ids(news_ids)
last_processed_date
    news_by_story = collections.defaultdict(set)
    for index, row in news.iterrows():
        news_by_story[row["story"]].add(row["id"])

    return news_by_story


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

        n_addition_events = 0
        n_change_events = 0
        n_deletion_events = 0

        # Add new clusters
        for cluster in new_clusters:
            cluster_id = db.add_cluster(cluster)
            db.add_event(Event.TOPIC_ADDED, cluster_id)
            n_addition_events += 1

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
            if "additions" in changes and len(changes["additions"]) > 0:
                n_change_events += 1
                db.add_event(Event.TOPIC_CHANGED, cluster_id, str(changes))

            if "deletions" in changes and len(changes["deletions"]) > 0:
                # We ignore deletions for now, since single batches might miss older articles, 
                # which we don't want to count as events. 
                pass

        # Get true events based on labeled test data
        new_news_ids = list(
            chain.from_iterable([identifier.split(",") for identifier in new_clusters])
        )
        existing_news_ids = list(
            chain.from_iterable(
                [identifier.split(",") for identifier in existing_clusters["identifier"]]
            )
        )

        new_rows = len(set(new_news_ids) - set(existing_news_ids))
        true_change_events, true_addition_events, true_deletion_events = find_true_events(
            new_news_ids, existing_news_ids
        )

        if verbose:
            print("----------------------")
            print("Statistics:")
            print("Number of changed clusters:", len(changed_clusters))
            print("Number of unchanged clusters:", len(unchanged_clusters))
            print("Number of new clusters:", len(new_clusters))
            print("----------------------")
            print("Events:")
            print("Topic added: {} detected, {} true".format(n_addition_events, true_addition_events))
            print("Topic changed: {} detected, {} true".format(n_change_events, len(true_change_events)))
            print("Topic deleted: {} detected, {} true".format(n_deletion_events, true_deletion_events))

        result = {
            "topic_added": {"detected": n_addition_events , "true": true_addition_events},
            "topic_changed": {"detected": n_change_events, "true": len(true_change_events)},
            "topic_deleted": {"detected": n_deletion_events , "true": true_deletion_events}
        }
        

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
        script_name, str(date), failed, log_message, processing_time, str(result), new_rows, full_cluster, rows
    )


# Test run:
# Single runs with partial clusters:
# * python data_processing/online_clustering.py --date "2014-03-11 00:00:00"
# * python data_processing/online_clustering.py --date "2014-03-11 12:00:00"
# * python data_processing/online_clustering.py --date "2014-03-12 12:00:00" --rows 2000
# * python data_processing/online_clustering.py --date "2014-03-12 13:00:00" --rows 2000
# * python data_processing/online_clustering.py --date "2014-03-13 12:00:00"
# * python data_processing/online_clustering.py --date "2014-03-13 13:00:00"
# Finally do a full cluster:
# * python data_processing/online_clustering.py --rows 5000


# Simulation:
# * python data_processing/online_clustering.py --date "2014-03-11 00:00:00" --run_n_days 2 --full_rows 10000 --rows 2000 --verbose
#  2014-05-01 might be a better date to start

# ToDos:
# Detect type of change:
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
    ap.add_argument("--full_rows", required=False, type=int, default=10000)
    ap.add_argument("--date", required=False, type=str, default=None)
    ap.add_argument("--run_n_days", required=False, type=int, default=0)
    ap.set_defaults(full_cluster=False)
    ap.set_defaults(verbose=False)
    args = vars(ap.parse_args())

    full_cluster = args["full_cluster"]
    rows = args["rows"]
    date = args["date"]
    verbose = args["verbose"]
    run_n_days = args["run_n_days"]
    full_rows = args["full_rows"]


    if run_n_days > 0:
        # run the simulation:
        db.reset_online_evaluation()
        current_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        end_date = current_date + timedelta(days=run_n_days)
        while current_date < end_date:

            if verbose:
                print()
                print("Date: ", current_date)
                
            if full_cluster and (current_date.hour == 0 or current_date.hour == 24):
                run(current_date, full_rows, True, verbose)
            else:
                run(current_date, rows, False, verbose)
                
            current_date += timedelta(hours=1)
        
    else:
        run(date, rows, full_cluster, verbose)
