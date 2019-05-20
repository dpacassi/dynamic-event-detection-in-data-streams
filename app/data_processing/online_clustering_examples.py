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

import online_clustering

script_name = os.path.basename(__file__)

load_dotenv()

def compare_clusters(existing_clusters, new_clusters):
        
    # Get true events based on labeled test data

    new_news_ids = list(
        chain.from_iterable([identifier.split(",") for identifier in new_clusters])
    )
    existing_news_ids = list(
        chain.from_iterable([identifier.split(",") for identifier in existing_clusters])
    )

    new_rows = len(set(new_news_ids) - set(existing_news_ids))
    true_change_events, true_addition_events, true_deletion_events = online_clustering.find_true_events(
        new_news_ids, existing_news_ids
    )

    changed_clusters, unchanged_clusters, new_clusters = online_clustering.find_changes_in_clusters(existing_clusters, new_clusters)

    print("----------------------")
    print("New Rows: ", len(set(new_news_ids) - set(existing_news_ids)))   
    print("Events:")
    print("Topic added: {} detected, {} true".format(len(new_clusters), true_addition_events))
    print("Topic extended: {} detected, {} true".format(len(changed_clusters), len(true_change_events)))


# Overwrite function to handle different input format... 



date1 = '2014-05-15 11:00:00'
date2 = '2014-05-15 12:00:00'
date3 = '2014-05-15 13:00:00'
date4 = '2014-05-15 14:00:00'
date5 = '2014-05-15 15:00:00'

nrows = 2000

clusters1,_ = online_clustering.cluster_news_by_date(nrows, date1)
clusters2,_ = online_clustering.cluster_news_by_date(nrows, date2)
clusters3,_ = online_clustering.cluster_news_by_date(nrows, date3)
clusters4,_ = online_clustering.cluster_news_by_date(nrows, date4)
clusters5,_ = online_clustering.cluster_news_by_date(nrows, date5)

compare_clusters(clusters1, clusters2)
compare_clusters(clusters2, clusters3)
compare_clusters(clusters3, clusters4)
compare_clusters(clusters4, clusters5)
