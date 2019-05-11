import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas
import json
import db
import collections

from  tabulate import tabulate
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()


# Processing time and accuracy for different clustering methods
def plot_different_clusterings():
    connection = db.get_connection()

    sql = (
        "select max(m.corrected_avg_unique_accuracy) as accuracy, avg(m.processing_time) as processing_time, m.method from method_evaluation as m"
        " where m.sample_size < 2000 and m.corrected_avg_unique_accuracy is not null"
        " group by m.method"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()
    fig = plt.figure()

    
    X = data["processing_time"].values
    Y = data["accuracy"].values

    colors = np.random.rand(len(X))
    plt.scatter(X, Y, c=colors, alpha=0.5)


    methods = data['method'].values
    for index, method in enumerate(methods):
        plt.annotate(method, (X[index], Y[index]), xytext = (X[index], Y[index] + 0.02))

    plt.ylim(top=1, bottom=0)
    plt.xlabel('Processing time in seconds')
    plt.ylabel('Accuracy')
    plt.title("Comparison of different clutering methods")
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.savefig('../../doc/images/different_clusterings.png')
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
    Y_hdbscan = data[data['method']=='hdbscan']["processing_time"].values
    Y_kmeans = data[data['method']=='kmeans']["processing_time"].values

    fig = plt.figure()
    plt.plot(X, Y_hdbscan, label='HDBSCAN')
    plt.plot(X, Y_kmeans, label='K-means')
    plt.xlabel('Number of news articles')
    plt.ylabel('Processing time in seconds')
    plt.yscale('log')
    plt.title("Average Processing Time by number of samples")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.savefig('../../doc/images/processing_time_kmeans_hdbscan.png')
    plt.close(fig)

# Accuracy by number of samples with hdbscan and kmeans
def plot_accuracy_samples():
    connection = db.get_connection()

    # Fixate hdbscan parameters and vectorizer for showing errors of best approach
    parameters = '{"min_cluster_size": 4, "metric": "cosine"}'
    vectorizer = 'TfidfVectorizer'
    sql = (
        "select m.corrected_avg_unique_accuracy as accuracy, m.real_clusters, m.method from method_evaluation as m"
        " where ((m.method = 'hdbscan' and m.parameters = %s) or m.method = 'kmeans') and m.corrected_avg_unique_accuracy is not null"
        " and vectorizer = %s"
        " and exists (select id from method_evaluation as m2 where m2.sample_size = m.sample_size and m2.method = 'kmeans') "
        " and exists (select id from method_evaluation as m3 where m3.sample_size = m.sample_size and m3.method = 'hdbscan') "
    )

    data = pandas.read_sql(sql=sql, con=connection, params=[parameters, vectorizer])
    connection.close()
    
    def format_data(data, method):
        accuracy_values = collections.defaultdict(list)
        for index, row in data.iterrows():
            if row["method"] == method:
                accuracy_values[row["real_clusters"]].append(row["accuracy"])
        
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

    X = data[data['method']=='hdbscan']["real_clusters"].values
    Y_hdbscan = data[data['method']=='hdbscan']["accuracy"].values
    Y_kmeans = data[data['method']=='kmeans']["accuracy"].values

    plt.scatter(X, Y_hdbscan, marker='o', label='HDBSCAN')
    plt.scatter(X, Y_kmeans, marker='^', label='K-means')

    # X = data["real_clusters"].unique()

    # Y, Y_lower_err, Y_higher_err = format_data(data, 'hdbscan')
    # plt.errorbar(X, Y, yerr=[Y_lower_err, Y_higher_err], fmt='o', label='HDBSCAN')

    # Y, Y_lower_err, Y_higher_err = format_data(data, 'kmeans')
    # plt.errorbar(X, Y, yerr=[Y_lower_err, Y_higher_err], fmt='^', label='K-means')

    plt.xlabel('Number of stories')
    plt.ylabel('Accuracy')
    plt.ylim(top=1, bottom=0)
    plt.title("Accuracy by number of stories")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.savefig('../../doc/images/accuracy_kmeans_hdbscan.png')
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
            Y_min_cluster_sizes[parameters["min_cluster_size"]] = collections.defaultdict(list)
        
        Y_min_cluster_sizes[parameters["min_cluster_size"]][row["sample_size"]].append(row["accuracy"])
        
    fig = plt.figure(figsize=(15,5))

    Y_cosine = [max(x) for x in cosine_values.values()]
    Y_euclidean = [max(x) for x in euclidean_values.values()]

    plt.subplot(1, 2, 1)
    plt.plot(X, Y_cosine, label='Cosine')
    plt.plot(X, Y_euclidean, label='Euclidean')
    plt.xlabel('Number of news articles')
    plt.ylabel('Average Accuracy')
    plt.ylim(top=1, bottom=0)
    plt.title("HDBSCAN Metrics")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)

    plt.subplot(1, 2, 2)

    for size, values in Y_min_cluster_sizes.items():
        Y = [max(x) for x in values.values()]
        if len(Y) < len(X):
            Y += [0] * (len(X) - len(Y))

        plt.plot(X, Y, label="m = {}".format(size))

    plt.xlabel('Number of news articles')
    plt.ylabel('Average Accuracy')
    plt.ylim(top=1, bottom=0)
    plt.title("HDBSCAN Min cluster sizes")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)

    plt.savefig('../../doc/images/hdbscan_parameters.png')
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
    plt.plot(X, Y_hdbscan, label='HDBSCAN')
    plt.xlabel('Number of news articles')
    plt.ylabel('Noise ratio')
    plt.ylim(top=1, bottom=0)
    plt.title("Ratio of samples classified as noise")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.savefig('../../doc/images/noise_ratio_samples.png')
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
    plt.plot(X, Y_hdbscan, label='HDBSCAN')
    plt.xlabel('Number of clusters')
    plt.ylabel('|n_true - n_predicted| / n_true')
    plt.ylim(top=0.1, bottom=0)
    plt.title("Difference in predicted number of clusters")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.savefig('../../doc/images/cluster_difference_samples.png')
    plt.close(fig)

# Detected events by date
def plot_event_detection_by_date():
    connection = db.get_connection()

    sql = (
        "select last_processed_date, result, new_rows, is_full_cluster from script_execution"
        " where failed = 0"
        " order by last_processed_date"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["last_processed_date"].values

    cosine_values = collections.defaultdict(list)
    euclidean_values = collections.defaultdict(list)
   
    Y_pred_add_events = []
    Y_pred_change_events = []
    Y_true_add_events = []
    Y_true_change_events = []

    for index, row in data.iterrows():
        result = json.loads(row["result"].replace("'", '"'))

        Y_pred_add_events.append(result["topic_added"]["detected"])
        Y_pred_change_events.append(result["topic_changed"]["detected"])
        Y_true_add_events.append(result["topic_added"]["true"])
        Y_true_change_events.append(result["topic_changed"]["true"])
        
    fig = plt.figure(figsize=(15,5))

    plt.subplot(1, 2, 1)
    plt.plot(X, Y_pred_add_events, label='Detected')
    plt.plot(X, Y_true_add_events, label='True')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()

    plt.xlabel('Time')
    plt.ylabel('Number of events')
    plt.title("Event: topic added")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)

    plt.subplot(1, 2, 2)

    plt.plot(X, Y_pred_change_events, label='Detected')
    plt.plot(X, Y_true_change_events, label='True')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()

    plt.xlabel('Time')    
    plt.ylabel('Number of events')
    plt.title("Event: topic changed")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)

    plt.savefig('../../doc/images/event_detection_by_date.png')
    plt.close(fig)


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

    plt.plot(X, Y_error_add, label='Error Additions')
    plt.plot(X, Y_error_change, label='Error Changes')

    plt.xlabel('Overlap')
    plt.ylabel('Detection Error')
    plt.title("Errors in detected events over cluster overlap")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)


    plt.savefig('../../doc/images/event_detection_overlap.png')
    plt.close(fig)

# TODO Accuracy by different vectorizer with hdbscan
# TODO Accuracy by different preprocessing and vectorizer with hdbscan

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
            table_dict[row["parameters"]][0] = row["parameters"].replace("{", "").replace("}", "").replace('"', "").replace('min_cluster', "min")

    table = table_dict.values()
    for row in table:
        max_index = np.argmax(row[1:])
        row[max_index + 1] = "aa" + "{:.3f}".format(row[max_index + 1]) + "bb"

    latex = tabulate(table, tablefmt="latex", floatfmt=".3f")
    latex = latex.replace("aa", "\\textbf{").replace("bb", "}")
    print(latex)


# Clustering method evaluation
# plot_accuracy_samples()
# plot_processing_time_samples()
# plot_cluster_difference_samples()
# plot_noise_ratio_samples()
# plot_different_clusterings()
# plot_hdbscan_parameters()
table_preprocessing()

# Online clustering evaluation
# plot_event_detection_by_date()
# plot_event_detection_overlap()