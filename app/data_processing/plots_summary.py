import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import numpy as np
import pandas
import json
import db
import collections
import statistics
import online_clustering

from matplotlib.collections import PatchCollection
from datetime import datetime
from datetime import timedelta
from tabulate import tabulate
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()


# Accuracy by number of samples with hdbscan and kmeans
def plot_hdbscan_kmeans(title, xlabel, ylabel, key):
    connection = db.get_connection()

    # Fixate hdbscan parameters and vectorizer for showing errors of best approach
    parameters = '{"min_cluster_size": 6, "metric": "cosine"}'
    vectorizer = "TfidfVectorizer"
    sql = (
        "select m.mp_score, m.real_clusters, m.method from method_evaluation as m"
        " where ((m.method = 'hdbscan' and parameters = %s) or m.method = 'kmeans') and m.mp_score is not null"
        " and vectorizer = %s and tokenizer != 'None'"
        " and exists (select id from method_evaluation as m2 where m2.sample_size = m.sample_size and m2.method = 'kmeans') "
        " and exists (select id from method_evaluation as m3 where m3.sample_size = m.sample_size and m3.method = 'hdbscan') "
       # " group by m.real_clusters, m.method "
    )

    data = pandas.read_sql(sql=sql, con=connection, params=[parameters, vectorizer])

    def _format_data(data, method):
        accuracy_values = collections.defaultdict(list)
        for index, row in data.iterrows():
            if row["method"] == method:
                accuracy_values[row["real_clusters"]].append(row["mp_score"])

        Y = []
        Y_lower_err = []
        Y_higher_err = []
        for key, values in accuracy_values.items():
            # It can be done more efficiently but this is only for a plot.
            avg = sum(values) / len(values)
            Y.append(avg)
            Y_lower_err.append(avg - min(values))
            Y_higher_err.append(max(values) - avg)

        return Y, Y_lower_err, Y_higher_err

    fig = plt.figure()

    # X = data[data["method"] == "hdbscan"]["real_clusters"].values
    # Y_hdbscan = data[data["method"] == "hdbscan"]["accuracy"].values
    # Y_kmeans = data[data["method"] == "kmeans"]["accuracy"].values

    # plt.scatter(X, Y_hdbscan, marker="o", label="HDBSCAN")
    # plt.scatter(X, Y_kmeans, marker="^", label="K-means")

    X = data["real_clusters"].unique()

    Y, Y_lower_err, Y_higher_err = _format_data(data, 'hdbscan')
    plt.errorbar(X, Y, yerr=[Y_lower_err, Y_higher_err], fmt='o', capsize=3, alpha=1, label='HDBSCAN')

    Y, Y_lower_err, Y_higher_err = _format_data(data, 'kmeans')
    plt.errorbar(X, Y, yerr=[Y_lower_err, Y_higher_err], fmt='^', capsize=3, alpha=1, label='k-means')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(top=1, bottom=0)
    plt.title(title)
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)

    plt.savefig("../../doc/images/summary/hdbscan_kmeans_{}.png".format(key))
    plt.close(fig)


# Detected events by date
def plot_event_detection_differences(title, xlabel, ylabel, key):
    connection = db.get_connection()

    sql = (
        "select last_processed_date, result, new_rows, is_full_cluster, nrows, mp_score from script_execution"
        " where failed = 0 and execution_date < '2019-05-28 14:00:00' and nrows is not null"
        " order by last_processed_date"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    fig, ax1 = plt.subplots()
    for nrow in [1000, 3000, 5000]:

        X = []
        Y_add = collections.defaultdict(list)
        Y_change = collections.defaultdict(list)

        for index, row in data.iterrows():
            result = json.loads(row["result"].replace("'", '"'))
            if row["nrows"] == nrow:
                
                day = row["last_processed_date"].strftime("%Y-%m-%d") 
                Y_add[day].append(abs(result["topic_added"]["detected"] - result["topic_added"]["true"]))
                Y_change[day].append(abs(result["topic_changed"]["detected"] - result["topic_changed"]["true"]))

        Y_lower_error = []
        Y_higher_error = []
        Y_median = []
        X = []
        for date, values in Y_add.items():
            X.append(datetime.strptime(date, "%Y-%m-%d"))
            Y_lower_error.append(min(values))
            Y_higher_error.append(max(values))
            Y_median.append(statistics.median(values))

        ax1.plot(X, Y_median, label="n={}".format(nrow))
        ax1.fill_between(X, Y_lower_error, Y_higher_error, alpha=0.3)
        # ax1.title("Difference in topic extended events")

    ax1.get_xaxis().set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax1.get_xaxis().set_major_locator(mdates.AutoDateLocator())

    plt.gcf().autofmt_xdate()

    # plt.ylim(top=100)
    ax1.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    ax1.legend()

    ax1.set_ylabel(ylabel)
    ax1.set_xlabel(xlabel)
    
    ax1.set_title(title)
    plt.savefig("../../doc/images/summary/event_detection_differences_{}.png".format(key))
    plt.close(fig)


plot_hdbscan_kmeans("MP-Score per Anzahl von Stories", "Anzahl von Stories", "MP-Score", "de")
plot_hdbscan_kmeans("MP-Score by number of stories", "Number of stories", "MP-Score", "en")
plot_event_detection_differences("Differenz zwischen erkannten und echten Ereignissen", "Zeit", "Anzahl von Ereignissen", "de")
plot_event_detection_differences("Difference between detected and true events", "Time",  "Number of events", "en")
