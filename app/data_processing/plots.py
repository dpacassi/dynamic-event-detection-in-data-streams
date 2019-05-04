import matplotlib.pyplot as plt
import pandas
import db
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

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
    plt.xlabel('Sample Size')
    plt.ylabel('Average Processing Time')
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
    plt.xlabel('Sample Size')
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
        "select avg(m.n_noise) as n_noise, m.sample_size from method_evaluation as m"
        " where m.method in ('hdbscan') and m.corrected_avg_unique_accuracy is not null"
        " group by m.sample_size"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["sample_size"].unique()
    Y_hdbscan = data["n_noise"].values

    fig = plt.figure()
    plt.plot(X, Y_hdbscan, label='HDBSCAN')
    plt.xlabel('Sample Size')
    plt.ylabel('Noise')
    plt.title("Noise Ratio")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.savefig('../../doc/images/noise_ratio_samples.png')
    plt.close(fig)

# HDBSCAN cluster difference
def plot_cluster_difference_samples():
    connection = db.get_connection()

    sql = (
        "select min(abs(m.real_clusters - m.estimated_clusters)) as diff, m.sample_size from method_evaluation as m"
        " where m.method in ('hdbscan') and m.corrected_avg_unique_accuracy is not null"
        " group by m.sample_size"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["sample_size"].unique()
    Y_hdbscan = data["diff"].values

    fig = plt.figure()
    plt.plot(X, Y_hdbscan, label='HDBSCAN')
    plt.xlabel('Sample Size')
    plt.ylabel('|n_true - n_predicted|')
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
# plot_hdbscan_parameters()