import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import numpy as np
import pandas
import json
import db
import collections
import statistics

from matplotlib.collections import PatchCollection
from datetime import datetime
from datetime import timedelta
from tabulate import tabulate
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()


# Processing time and accuracy for different clustering methods
def plot_different_clusterings():
    connection = db.get_connection()

    sql = (
        "select max(m.mp_score), avg(m.processing_time) as processing_time, m.method from method_evaluation as m"
        " where m.sample_size < 2000 and m.mp_score is not null"
        " group by m.method"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()
    fig = plt.figure()

    X = data["processing_time"].values
    Y = data["mp_score"].values

    colors = np.random.rand(len(X))
    plt.scatter(X, Y, c=colors, alpha=0.5)

    methods = data["method"].values
    for index, method in enumerate(methods):
        plt.annotate(method, (X[index], Y[index]), xytext=(X[index], Y[index] + 0.02))

    plt.ylim(top=1, bottom=0)
    plt.xlabel("Processing time in seconds")
    plt.ylabel("Accuracy")
    plt.title("Comparison of different clutering methods")
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    plt.savefig("../../doc/images/different_clusterings.png")
    plt.close(fig)


# Processing time by number of samples with hdbscan and kmeans
def plot_processing_time_samples():
    connection = db.get_connection()

    sql = (
        "select avg(m.processing_time) as processing_time, m.sample_size, m.method from method_evaluation as m"
        " where m.method in ('kmeans', 'hdbscan') and m.corrected_avg_unique_accuracy is not null"
        " and exists (select id from method_evaluation as m2 where m2.sample_size = m.sample_size and m2.method = 'kmeans') "
        " and exists (select id from method_evaluation as m3 where m3.sample_size = m.sample_size and m3.method = 'hdbscan') "
        " group by m.sample_size, m.method"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["sample_size"].unique()
    Y_hdbscan = data[data["method"] == "hdbscan"]["processing_time"].values
    Y_kmeans = data[data["method"] == "kmeans"]["processing_time"].values

    fig = plt.figure()
    plt.plot(X, Y_hdbscan, label="HDBSCAN")
    plt.plot(X, Y_kmeans, label="K-means")
    plt.xlabel("Number of news articles")
    plt.ylabel("Processing time in seconds")
    plt.yscale("log")
    plt.xscale("log")

    k = np.array(Y_hdbscan.argmax())
    plt.text(X[k],Y_hdbscan[k], round(Y_hdbscan[k], 0))
    
    k = np.array(Y_kmeans.argmax())
    plt.text(X[k],Y_kmeans[k], round(Y_kmeans[k], 0))

    plt.title("Average Processing Time by number of samples")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    plt.savefig("../../doc/images/processing_time_kmeans_hdbscan.png")
    plt.close(fig)


# Accuracy by number of samples with hdbscan and kmeans
def plot_accuracy_samples():
    connection = db.get_connection()

    # Fixate hdbscan parameters and vectorizer for showing errors of best approach
    parameters = '{"min_cluster_size": 5, "metric": "cosine"}'
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
    connection.close()

    def format_data(data, method):
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

    Y, Y_lower_err, Y_higher_err = format_data(data, 'hdbscan')
    plt.errorbar(X, Y, yerr=[Y_lower_err, Y_higher_err], fmt='o', capsize=3, label='HDBSCAN')

    Y, Y_lower_err, Y_higher_err = format_data(data, 'kmeans')
    plt.errorbar(X, Y, yerr=[Y_lower_err, Y_higher_err], fmt='^', capsize=3, label='K-means')

    plt.xlabel("Number of stories")
    plt.ylabel("MP-Score")
    plt.ylim(top=1, bottom=0)
    plt.title("MP-Score by number of stories")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    plt.savefig("../../doc/images/accuracy_kmeans_hdbscan.png")
    plt.close(fig)


# Accuracy by different parameters with hdbscan
def plot_hdbscan_parameters():
    connection = db.get_connection()

    sql = (
        "select max(m.corrected_avg_unique_accuracy) as accuracy, m.parameters, m.sample_size from method_evaluation as m"
        " where m.method = 'hdbscan' and m.corrected_avg_unique_accuracy is not null"
        " group by m.parameters, m.sample_size"
        " order by m.sample_size"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["sample_size"].unique()

    cosine_values = collections.defaultdict(list)
    euclidean_values = collections.defaultdict(list)
    Y_min_cluster_sizes = dict()

    for index, row in data.iterrows():
        parameters = json.loads(row["parameters"])
        if parameters["metric"] == "cosine":
            cosine_values[row["sample_size"]].append(row["accuracy"])
        if parameters["metric"] == "euclidean":
            euclidean_values[row["sample_size"]].append(row["accuracy"])

        if parameters["min_cluster_size"] not in Y_min_cluster_sizes:
            Y_min_cluster_sizes[
                parameters["min_cluster_size"]
            ] = collections.defaultdict(list)

        Y_min_cluster_sizes[parameters["min_cluster_size"]][row["sample_size"]].append(
            row["accuracy"]
        )

    fig = plt.figure(figsize=(15, 5))

    Y_cosine = [max(x) for x in cosine_values.values()]
    Y_euclidean = [max(x) for x in euclidean_values.values()]

    plt.subplot(1, 2, 1)
    plt.plot(X, Y_cosine, label="Cosine")
    plt.plot(X, Y_euclidean, label="Euclidean")
    plt.xlabel("Number of news articles")
    plt.ylabel("Average Accuracy")
    plt.ylim(top=1, bottom=0)
    plt.title("HDBSCAN Metrics")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)

    plt.subplot(1, 2, 2)

    for size, values in Y_min_cluster_sizes.items():
        Y = [max(x) for x in values.values()]
        if len(Y) < len(X):
            Y += [0] * (len(X) - len(Y))

        plt.plot(X, Y, label="m = {}".format(size))

    plt.xlabel("Number of news articles")
    plt.ylabel("Average Accuracy")
    plt.ylim(top=1, bottom=0)
    plt.title("HDBSCAN Min cluster sizes")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)

    plt.savefig("../../doc/images/hdbscan_parameters.png")
    plt.close(fig)


# HDBSCAN Noise ratio with number of samples
def plot_noise_ratio_samples():
    connection = db.get_connection()

    # TODO with different min_cluster_sizes
    sql = (
        "select min(m.n_noise / m.sample_size) as n_noise, m.sample_size from method_evaluation as m"
        " where m.method in ('hdbscan') and m.corrected_avg_unique_accuracy is not null"
        " group by m.sample_size"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["sample_size"].unique()
    Y_hdbscan = data["n_noise"].values

    fig = plt.figure()
    plt.plot(X, Y_hdbscan, label="HDBSCAN")
    plt.xlabel("Number of news articles")
    plt.ylabel("Noise ratio")
    plt.ylim(top=1, bottom=0)
    plt.title("Ratio of samples classified as noise")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    plt.savefig("../../doc/images/noise_ratio_samples.png")
    plt.close(fig)


# HDBSCAN cluster difference
def plot_cluster_difference_samples():
    connection = db.get_connection()

    sql = (
        "select min(abs(m.real_clusters - m.estimated_clusters) / m.real_clusters) as diff, m.real_clusters from method_evaluation as m"
        " where m.method in ('hdbscan') and m.corrected_avg_unique_accuracy is not null"
        " group by m.real_clusters"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["real_clusters"].unique()
    Y_hdbscan = data["diff"].values

    fig = plt.figure()
    plt.plot(X, Y_hdbscan, label="HDBSCAN")
    plt.xlabel("Number of clusters")
    plt.ylabel("|n_true - n_predicted| / n_true")
    plt.ylim(top=0.1, bottom=0)
    plt.title("Difference in predicted number of clusters")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    plt.savefig("../../doc/images/cluster_difference_samples.png")
    plt.close(fig)


# Detected events by date
def plot_event_detection_by_date():
    connection = db.get_connection()

    sql = (
        "select last_processed_date, result, new_rows, is_full_cluster, nrows, mp_score from script_execution"
        " where failed = 0 and execution_date < '2019-05-28 14:00:00'"
        " order by last_processed_date"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    nrows = data["nrows"].unique()
    for nrow in nrows:

        X = []
        Y_pred_add_events = []
        Y_pred_change_events = []
        Y_true_add_events = []
        Y_true_change_events = []
        Y_mp_score = []
        Y_add = collections.defaultdict(list)
        Y_change = collections.defaultdict(list)
        Y_change_mp_score = []
        Y_add_mp_score = []

        for index, row in data.iterrows():
            result = json.loads(row["result"].replace("'", '"'))
            if row["nrows"] == nrow:
                X.append(row["last_processed_date"])

                Y_pred_add_events.append(result["topic_added"]["detected"])
                Y_pred_change_events.append(result["topic_changed"]["detected"])
                Y_true_add_events.append(result["topic_added"]["true"])
                Y_true_change_events.append(result["topic_changed"]["true"])
                Y_mp_score.append(row["mp_score"])

                Y_change_mp_score.append(result["topic_changed"]["mp_score"])
                Y_add_mp_score.append(result["topic_added"]["mp_score"])

                day = row["last_processed_date"].strftime("%Y-%m-%d") 
                Y_add[day].append(abs(result["topic_added"]["detected"] - result["topic_added"]["true"]))
                Y_change[day].append(abs(result["topic_changed"]["detected"] - result["topic_changed"]["true"]))

        # Remove first entry, because the inital batch skews the scale for new topics.
        Y_pred_add_events[0] = 0
        Y_true_add_events[0] = 0
        Y_add[0] = 0

        fig = plt.figure(figsize=(15, 5))

        plt.subplot(1, 2, 1)
       
        plt.plot(X, Y_pred_add_events,  '.', label="Detected")
        plt.plot(X, Y_true_add_events,  '.', label="True")
        plt.ylim(top=50)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gcf().autofmt_xdate()

        plt.xlabel("Time")
        plt.ylabel("Number of events")
        plt.title("New Topics")
        plt.legend()
        plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
        
        #####
        plt.subplot(1, 2, 2)

        plt.plot(X, Y_pred_change_events,  '.', label="Detected")
        plt.plot(X, Y_true_change_events,  '.', label="True")
        plt.ylim(top=120)

        plt.ylabel("Number of events")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gcf().autofmt_xdate()

        plt.xlabel("Time")
        plt.title("Topics extended")
        plt.legend()
        plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
        
        plt.savefig("../../doc/images/event_detection_by_date_{}.png".format(nrow))
        plt.close(fig)


# Detected events by date
def plot_event_detection_differences():
    connection = db.get_connection()

    sql = (
        "select last_processed_date, result, new_rows, is_full_cluster, nrows, mp_score from script_execution"
        " where failed = 0 and execution_date < '2019-05-28 14:00:00'"
        " order by last_processed_date"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    nrows = data["nrows"].unique()
    for nrow in [1000,3000,5000]:

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

        Y_lower_error = []
        Y_higher_error = []
        Y_median = []
        for date, values in Y_change.items():
            Y_lower_error.append(min(values))
            Y_higher_error.append(max(values))
            Y_median.append(statistics.median(values))

        ax2.plot(X, Y_median, label="n={}".format(nrow))
        ax2.fill_between(X, Y_lower_error, Y_higher_error, alpha=0.3)
        # ax2.title("Difference in topic extended events")

    ax1.get_xaxis().set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax1.get_xaxis().set_major_locator(mdates.AutoDateLocator())

    ax2.get_xaxis().set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax2.get_xaxis().set_major_locator(mdates.AutoDateLocator())
    
    plt.gcf().autofmt_xdate()

    plt.ylim(top=100)
    ax1.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    ax1.legend()
    ax1.set_title("Difference in new topic detections vs ground truth")
    ax1.set_ylabel("Number of events")
    ax2.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    ax2.legend()
    ax2.set_title("Difference in topic extension detections vs ground truth")
    ax2.set_ylabel("Number of events")
    plt.savefig("../../doc/images/event_detection_differences.png")
    plt.close(fig)

def plot_event_detection_differences_with_threshold():
    connection = db.get_connection()

    sql = (
        "select last_processed_date, result, new_rows, is_full_cluster, nrows, mp_score, threshold from script_execution"
        " where failed = 0"
        " order by last_processed_date"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    nrows = data["nrows"].unique()
    for nrow in [0.75,0.5,0.1]:

        X = []
        Y_add = collections.defaultdict(list)
        Y_change = collections.defaultdict(list)

        for index, row in data.iterrows():
            result = json.loads(row["result"].replace("'", '"'))
            if row["threshold"] == nrow:
                
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

        ax1.plot(X, Y_median, label="threshold={}".format(nrow))
        ax1.fill_between(X, Y_lower_error, Y_higher_error, alpha=0.3)
        # ax1.title("Difference in topic extended events")

        Y_lower_error = []
        Y_higher_error = []
        Y_median = []
        for date, values in Y_change.items():
            Y_lower_error.append(min(values))
            Y_higher_error.append(max(values))
            Y_median.append(statistics.median(values))

        ax2.plot(X, Y_median, label="threshold={}".format(nrow))
        ax2.fill_between(X, Y_lower_error, Y_higher_error, alpha=0.3)
        # ax2.title("Difference in topic extended events")

    ax1.get_xaxis().set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax1.get_xaxis().set_major_locator(mdates.AutoDateLocator())

    ax2.get_xaxis().set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax2.get_xaxis().set_major_locator(mdates.AutoDateLocator())
    
    plt.gcf().autofmt_xdate()

    plt.ylim(top=100)
    ax1.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    ax1.legend()
    ax1.set_title("Difference in new topic detections vs ground truth")
    ax1.set_ylabel("Number of events")
    ax2.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    ax2.legend()
    ax2.set_title("Difference in topic extension detections vs ground truth")
    ax2.set_ylabel("Number of events")
    plt.savefig("../../doc/images/event_detection_differences_threshold.png")
    plt.close(fig)


def plot_event_detection_differences_with_cluster_size():
    connection = db.get_connection()

    sql = (
        "select last_processed_date, result, new_rows, is_full_cluster, nrows, mp_score, execution_date from script_execution"
        " where failed = 0 and nrows = 3000"
        " order by last_processed_date"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    fig, ax1 = plt.subplots()

    nrows = data["nrows"].unique()

    # hacky but this is only for one time use.
    for run in [0,1]:

        X = []
        Y_add = collections.defaultdict(list)
        Y_change = collections.defaultdict(list)

        for index, row in data.iterrows():
            ts = pandas.Timestamp(2019, 5, 28, 14)
            if ((run == 0 and row["execution_date"] < ts)
                or (run == 1 and row["execution_date"] > ts)) :
                result = json.loads(row["result"].replace("'", '"'))

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

        ax1.plot(X, Y_median, label="n=3000")
        ax1.fill_between(X, Y_lower_error, Y_higher_error, alpha=0.3)
        # ax1.title("Difference in topic extended events")

    ax1.get_xaxis().set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax1.get_xaxis().set_major_locator(mdates.AutoDateLocator())
    
    plt.gcf().autofmt_xdate()
    ax1.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
    ax1.legend()
    ax1.set_title("Difference in new topic detections vs ground truth")
    ax1.set_ylabel("Number of events")
    plt.savefig("../../doc/images/event_detection_differences_with_min_cluster_size.png")
    plt.close(fig)


# Detected events by date
def plot_mp_scores_for_event_detection_by_date():
    connection = db.get_connection()

    sql = (
        "select last_processed_date, result, new_rows, is_full_cluster, nrows, mp_score from script_execution"
        " where failed = 0 and threshold < 0.2"
        " order by last_processed_date"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    nrows = data["nrows"].unique()
    for nrow in nrows:

        cosine_values = collections.defaultdict(list)
        euclidean_values = collections.defaultdict(list)

        Y_mp_score = collections.defaultdict(list)
        Y_change_mp_score = collections.defaultdict(list)
        Y_add_mp_score = collections.defaultdict(list)
        X = dict()

        for index, row in data.iterrows():
            result = json.loads(row["result"].replace("'", '"'))
            if row["nrows"] == nrow:
                day = row["last_processed_date"].strftime("%Y-%m-%d") 
                X[day] = row["last_processed_date"].strftime("%d.%m.")
                Y_mp_score[day].append(row["mp_score"])

                Y_change_mp_score[day].append(result["topic_changed"]["mp_score"])
                Y_add_mp_score[day].append(result["topic_added"]["mp_score"])


        fig = plt.figure(figsize=(20, 5))

        #####
        plt.subplot( 1, 3, 1)

        plt.boxplot(Y_mp_score.values())
        plt.ylim(top=1, bottom=0)

        plt.title("Overall MP-Score")
        plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
        replace_x_ticks_with_date(plt, X)

        #####
        plt.subplot(1, 3, 2)

        plt.boxplot(Y_add_mp_score.values())
        plt.ylim(top=1, bottom=0)

        plt.title("MP-Score of new topics")
        plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)
        replace_x_ticks_with_date(plt, X)

        #####
        plt.subplot(1, 3, 3)

        plt.boxplot(Y_change_mp_score.values())
        plt.ylim(top=1, bottom=0)

        plt.title("MP-Score of extended topic")
        plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)

        # hide every second tick and replace with date labels
        replace_x_ticks_with_date(plt, X)

        plt.gcf().autofmt_xdate()

        plt.savefig("../../doc/images/event_detection_mp_score_{}_0_1.png".format(nrow))
        plt.close(fig)


def replace_x_ticks_with_date(plt, X):     
    loc, labels = plt.xticks()
    plt.xticks(loc, X.values())
    for label in plt.gca().xaxis.get_ticklabels()[::2]:
        label.set_visible(False)


def plot_event_detection_overlap():
    connection = db.get_connection()

    sql = (
        "select (nrows - new_rows) / nrows as overlap, result, new_rows, nrows, is_full_cluster from script_execution"
        " where failed = 0"
        " order by overlap"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["overlap"].values

    Y_error_add = []
    Y_error_change = []

    for index, row in data.iterrows():
        result = json.loads(row["result"].replace("'", '"'))

        topics_added = result["topic_added"]
        topic_changed = result["topic_changed"]

        Y_error_add.append(abs(topics_added["detected"] - topics_added["true"]))
        Y_error_change.append(abs(topic_changed["detected"] - topic_changed["true"]))

    fig = plt.figure()

    plt.plot(X, Y_error_add, label="Error Additions")
    plt.plot(X, Y_error_change, label="Error Changes")

    plt.xlabel("Overlap")
    plt.ylabel("Detection Error")
    plt.title("Errors in detected events over cluster overlap")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)

    plt.savefig("../../doc/images/event_detection_overlap.png")
    plt.close(fig)


# TODO Accuracy by different vectorizer with hdbscan
# TODO Accuracy by different preprocessing and vectorizer with hdbscan


def plot_articles_per_story_distribution():
    connection = db.get_connection()

    sql = (
        "SELECT count(n.id) as narticles, n.story FROM news_article as n"
        " group by n.story "
        " order by narticles"
    )

    data = pandas.read_sql(sql=sql, con=connection)

    fig = plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)

    plt.hist(data["narticles"], bins='auto')

    plt.xlabel("Number of articles")
    plt.ylabel("Number of stories")
    plt.title("Distribution of articles per story")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)

    plt.subplot(1, 3, 2)

    plt.hist(data["narticles"], bins='auto', range=[1, 100])

    plt.xlabel("Number of articles")
    plt.ylabel("Number of stories")
    plt.title("Distribution of articles per story < 100")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)

    plt.subplot(1, 3, 3)

    plt.hist(data["narticles"], bins='auto', range=[0, 10])

    plt.xlabel("Number of articles")
    plt.ylabel("Number of stories")
    plt.title("Distribution of articles per story < 10")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)


    plt.savefig("../../doc/images/articles_per_story_distribution.png")
    plt.close(fig)


def table_preprocessing():
    connection = db.get_connection()

    sql = (
        "select m.corrected_avg_unique_accuracy as accuracy, m.parameters, m.real_clusters, tokenizer, vectorizer from method_evaluation as m"
        " where  m.method in ('kmeans', 'hdbscan') and m.corrected_avg_unique_accuracy is not null and tokenizer != 'None'"
        " order by m.parameters"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    table_dict = collections.defaultdict(list)

    indicies = {
        "CountVectorizer_newspaper_text": 1,
        "CountVectorizer_text_keyterms": 2,
        "CountVectorizer_text_entities": 3,
        "CountVectorizer_text_lemmatized_without_stopwords": 4,
        "CountVectorizer_text_stemmed_without_stopwords": 5,
        "TfidfVectorizer_newspaper_text": 6,
        "TfidfVectorizer_text_keyterms": 7,
        "TfidfVectorizer_text_entities": 8,
        "TfidfVectorizer_text_lemmatized_without_stopwords": 9,
        "TfidfVectorizer_text_stemmed_without_stopwords": 10,
    }

    for index, row in data.iterrows():
        if len(table_dict[row["parameters"]]) == 0:
            table_dict[row["parameters"]] = [0 for x in range(len(indicies) + 1)]

        key = row["vectorizer"] + "_" + row["tokenizer"]
        if key in indicies:
            table_dict[row["parameters"]][indicies[key]] = round(row["accuracy"], 3)
            table_dict[row["parameters"]][0] = (
                row["parameters"]
                .replace("{", "")
                .replace("}", "")
                .replace('"', "")
                .replace("min_cluster", "min")
            )

    table = table_dict.values()
    for row in table:
        max_index = np.argmax(row[1:])
        row[max_index + 1] = "aa" + "{:.3f}".format(row[max_index + 1]) + "bb"

    latex = tabulate(table, tablefmt="latex", floatfmt=".3f")
    latex = latex.replace("aa", "\\textbf{").replace("bb", "}")
    print(latex)


def plot_news_article_distribution_per_day():
    connection = db.get_connection()

    start_date = '2014-05-08 00:00:00'
    end_date = '2014-06-06 23:00:00'

    sql = (
        "SELECT count(id) as narticles, CAST(computed_publish_date AS DATE) as day FROM news_article"
        " where computed_publish_date >= %s and computed_publish_date <= %s"
        " group by CAST(computed_publish_date AS DATE) "
        " order by CAST(computed_publish_date AS DATE) "
    )

    data = pandas.read_sql(sql=sql, con=connection, params=[start_date, end_date])

    fig = plt.figure()

    plt.bar(data["day"], data["narticles"])

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()

    plt.xlabel("Time")
    plt.ylabel("Number of news articles")
    plt.title("News article distribution over time")
    plt.legend()
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)

    plt.savefig("../../doc/images/news_articles_over_time.png")
    plt.close(fig)


def plot_online_clustering_example(story, keyword):
    connection = db.get_connection()

    sql = (
        "select id, computed_publish_date, title, story from news_article"
        " where story = %s and preprocessed = 1 order by computed_publish_date asc"
    )

    data = pandas.read_sql(sql=sql, con=connection, params=[story])

    articles = collections.defaultdict(int)
    articles_ids = collections.defaultdict(list)
    article_position_by_id = dict()

    dates = data["computed_publish_date"].values
    patches = []

    current_time = datetime.fromtimestamp(dates[0].astype(datetime)  / 1e9)
    end_time = datetime.fromtimestamp(dates[-1].astype(datetime)  / 1e9)

    while current_time < end_time:
        current_hour = current_time.strftime("%d.%m %H:00") 
        articles[current_hour] = 0
        current_time += timedelta(hours=1)

    for i, date in enumerate(dates):
        data_hour = datetime.fromtimestamp(date.astype(datetime) / 1e9).strftime("%d.%m %H:00") 
        articles[data_hour] += 50
        articles_ids[data_hour].append(data["id"].values[i])

    X = articles.keys()
    Y = [1]*len(X)
    S = list(articles.values())
    blue_points = [0]*len(X)

    # prepare coordinates
    for i, hour in enumerate(articles):
        if hour in articles_ids:
            for article_id in articles_ids[hour]:
                article_position_by_id[article_id] = i

    
    event_sql = (
        "select event.id as event_id, news_article.id as news_id, event.type as event_type from event"
        " join cluster_news_article on cluster_news_article.cluster_id = event.cluster_id"
        " join cluster on cluster.id = event.cluster_id"
        " join news_article on cluster_news_article.news_article_id = news_article.id and news_article.story = %s and preprocessed = 1"
        " where event.insert_date > '2019-05-30 09:00:00'"
        " order by event.insert_date, news_article.computed_publish_date asc"
    )

    event_data = pandas.read_sql(sql=event_sql, con=connection, params=[story])

    events = collections.defaultdict(list)
    colors = dict()
    for index, row in event_data.iterrows():
        events[row["event_id"]].append(row["news_id"])

        if row["event_type"] == 1:
            colors[row["event_id"]] = "tab:green"
        else:
            colors[row["event_id"]] = "tab:blue"

    height = 0.0005
    decrement = 0.0008

    y_pos = 1 + (len(events)-1) / 2 * (decrement)

    draw = True
    for key, values in events.items():
        values.sort(key=lambda x: article_position_by_id[x])
        # we are only interested in complete events
        if values[0] in article_position_by_id:
            start_x = article_position_by_id[values[0]]
            length = article_position_by_id[values[-1]] - start_x + 1

            for value in values:
                index = article_position_by_id[value]
                blue_points[index] = S[index]

            #if start_x > 0 or draw:
            rect = mpatches.Rectangle([start_x - 0.5, y_pos], length, height)
            patches.append(rect)

            y_pos -= decrement
        # height += increment

    fig = plt.figure(figsize=(15, 8))

    #plt.ylim(bottom=0.985, top=1.035)
    plt.yticks([])

    collection = PatchCollection(patches, color=list(colors.values()), alpha=0.3)
    ax = plt.gca()
    ax.add_collection(collection)

    plt.scatter(X, Y, s=S, c="black")
    plt.scatter(X, Y, s=blue_points)

    plt.gcf().autofmt_xdate()

    for label in plt.gca().xaxis.get_ticklabels()[::2]:
        label.set_visible(False)

    plt.title("News articles and clusters of a single story")
    plt.grid(True, "major", ls="--", lw=0.5, c="k", alpha=0.3)

    if len(patches) > 0:
        plt.savefig("../../doc/images/online_clustering_example_{}.png".format(story
        ))
    plt.close(fig)


# Clustering method evaluation
# plot_accuracy_samples()
# plot_processing_time_samples()
# plot_cluster_difference_samples()
# plot_noise_ratio_samples()
# plot_different_clusterings()
# plot_hdbscan_parameters()
# table_preprocessing()
# plot_articles_per_story_distribution()

# Online clustering evaluation
# plot_news_article_distribution_per_day()
# plot_event_detection_by_date()
# plot_event_detection_differences()
# plot_event_detection_differences_with_threshold()
# plot_event_detection_differences_with_cluster_size()
# plot_mp_scores_for_event_detection_by_date()
# plot_event_detection_overlap()
#plot_online_clustering_example(story = 'dTEqnWhDkbceWsMQa07JPBzkaYb3M', keyword="gmail")
#plot_online_clustering_example(story = 'dMz8NzNxiPqTctM7zwUCIuAs__DyM', keyword="hillshire")

# connection = db.get_connection()

# sql = "select story from news_article WHERE newspaper_processed = 1 AND title_keywords_intersection = 1 AND newspaper_text IS NOT NULL and preprocessed = 1 and CAST(computed_publish_date AS DATE) > '2014-05-10' and CAST(computed_publish_date AS DATE) < '2014-06-01' GROUP BY  story HAVING count(id) > 20 and count(id) < 40"

# data = pandas.read_sql(sql=sql, con=connection)
# print(len(data))
# for i, story in enumerate(data["story"].values):
#     print(i)
#     plot_online_clustering_example(story, i)

