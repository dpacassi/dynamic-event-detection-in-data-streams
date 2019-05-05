import matplotlib.pyplot as plt
import numpy as np
import pandas
import db
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
    plt.title("Average Processing Time by number of samples")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.savefig('../../doc/images/processing_time_kmeans_hdbscan.png')
    plt.close(fig)

# Accuracy by number of samples with hdbscan and kmeans
def plot_accuracy_samples():
    connection = db.get_connection()

    sql = (
        "select max(m.corrected_avg_unique_accuracy) as accuracy, m.sample_size, m.method from method_evaluation as m"
        " where m.method in ('kmeans', 'hdbscan') and m.corrected_avg_unique_accuracy is not null"
        " and exists (select id from method_evaluation as m2 where m2.sample_size = m.sample_size and m2.method = 'kmeans') "
        " and exists (select id from method_evaluation as m3 where m3.sample_size = m.sample_size and m3.method = 'hdbscan') "
        " group by m.sample_size, m.method"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["sample_size"].unique()
    Y_hdbscan = data[data['method']=='hdbscan']["accuracy"].values
    Y_kmeans = data[data['method']=='kmeans']["accuracy"].values

    fig = plt.figure()
    plt.plot(X, Y_hdbscan, label='HDBSCAN')
    plt.plot(X, Y_kmeans, label='K-means')
    plt.xlabel('Number of news articles')
    plt.ylabel('Average Accuracy')
    plt.ylim(top=1, bottom=0)
    plt.title("Accuracy by number of samples")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.savefig('../../doc/images/accuracy_kmeans_hdbscan.png')
    plt.close(fig)

# TODO Accuracy by different parameters with hdbscan
def plot_hdbscan_parameters():
    connection = db.get_connection()

    sql = (
        "select avg(m.corrected_avg_unique_accuracy) as accuracy, m.parameters from method_evaluation as m"
        " where m.method = 'hdbscan' and m.corrected_avg_unique_accuracy is not null"
        " group by m.parameters"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["accuracy"].values
    Y = data["parameters"].values

    plt.barh(X, Y, label='HDBSCAN')
    plt.xlabel('Parameters')
    plt.ylabel('Average Accuracy')
    plt.xlim(right=1, left=0)
    plt.title("HDBSCAN Parameters")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.show()


# HDBSCAN Noise ratio with number of samples
def plot_noise_ratio_samples():
    connection = db.get_connection()

    # TODO with different min_cluster_sizes
    sql = (
        "select avg(m.n_noise / m.sample_size) as n_noise, m.sample_size from method_evaluation as m"
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


# TODO Accuracy by different vectorizer with hdbscan
# TODO Accuracy by different preprocessing and vectorizer with hdbscan

plot_accuracy_samples()
plot_processing_time_samples()
plot_cluster_difference_samples()
plot_noise_ratio_samples()
plot_different_clusterings()
# plot_hdbscan_parameters()