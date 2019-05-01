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
        " where m.method in ('kmeans', 'hdbscan') and m.avg_unique_accuracy is not null"
        " and exists (select id from method_evaluation as m2 where m2.sample_size = m.sample_size and m2.method = 'kmeans') "
        " and exists (select id from method_evaluation as m3 where m3.sample_size = m.sample_size and m3.method = 'hdbscan') "
        " group by m.sample_size, m.method"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["sample_size"].unique()
    Y_hdbscan = data[data['method']=='hdbscan']["processing_time"].values
    Y_kmeans = data[data['method']=='kmeans']["processing_time"].values

    plt.plot(X, Y_hdbscan, label='HDBSCAN')
    plt.plot(X, Y_kmeans, label='K-means')
    plt.xlabel('Sample Size')
    plt.ylabel('Average Processing Time')
    plt.title("Average Processing Time by number of samples")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.show()

# Accuracy by number of samples with hdbscan and kmeans
def plot_accuracy_samples():
    connection = db.get_connection()

    sql = (
        "select max(m.avg_unique_accuracy) as accuracy, m.sample_size, m.method from method_evaluation as m"
        " where m.method in ('kmeans', 'hdbscan') and m.avg_unique_accuracy is not null"
        " and exists (select id from method_evaluation as m2 where m2.sample_size = m.sample_size and m2.method = 'kmeans') "
        " and exists (select id from method_evaluation as m3 where m3.sample_size = m.sample_size and m3.method = 'hdbscan') "
        " group by m.sample_size, m.method"
    )

    data = pandas.read_sql(sql=sql, con=connection)
    connection.close()

    X = data["sample_size"].unique()
    Y_hdbscan = data[data['method']=='hdbscan']["accuracy"].values
    Y_kmeans = data[data['method']=='kmeans']["accuracy"].values

    plt.plot(X, Y_hdbscan, label='HDBSCAN')
    plt.plot(X, Y_kmeans, label='K-means')
    plt.xlabel('Sample Size')
    plt.ylabel('Average Accuracy')
    plt.ylim(top=1, bottom=0)
    plt.title("Accuracy by number of samples")
    plt.legend()
    plt.grid(True, 'major',  ls='--', lw=.5, c='k', alpha=.3)
    plt.show()

# TODO Accuracy by different parameters with hdbscan
def plot_hdbscan_parameters():
    connection = db.get_connection()

    sql = (
        "select max(m.avg_unique_accuracy) as accuracy, m.parameters from method_evaluation as m"
        " where m.method = 'hdbscan' and m.avg_unique_accuracy is not null"
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

# TODO Accuracy by different vectorizer with hdbscan
# TODO Noise ratio with hdbscan
# TODO Accuracy by different preprocessing and vectorizer with hdbscan


plot_accuracy_samples()
plot_processing_time_samples()
# plot_hdbscan_parameters()