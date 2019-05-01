import os
import sys
import pymysql
import subprocess
from dotenv import load_dotenv

######################################################################################
# Check if the script is already running.
######################################################################################

script_names = ['define_cluster_evaluations.py']

for script_name in script_names:
    status = subprocess.getstatusoutput(
        "ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'| awk '{print $2}'" % script_name
    )
    if status[1]:
        sys.exit(0)

# Load environment variables.
load_dotenv()

connection = pymysql.connect(
    host=os.environ['MYSQL_HOSTNAME'],
    port=int(os.environ['MYSQL_PORT']),
    user=os.environ['MYSQL_USER'],
    passwd=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

truncate_sql = "TRUNCATE TABLE cron_evaluation"
insert_sql = (
    "INSERT INTO cron_evaluation"
    " (method, `rows`, skip_rows, vectorizer, tokenizer, parameters, normalized_mutual_info_score, adjusted_mutual_info_score, completeness_score, estimated_clusters, real_clusters, n_noise, time_clustering, time_preprocessing, time_total, processed, failed)"
    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)


######################################################################################
# Base configuration.
######################################################################################

rows = [1000, 2000, 3000]
chunks = 3
preprocessings = [
    {'skip_text_preprocessing': True},
    {'skip_text_preprocessing': False, 'use_stemming': True, 'use_lemmatization': False, 'keep_stopwords': False},
    {'skip_text_preprocessing': False, 'use_stemming': True, 'use_lemmatization': False, 'keep_stopwords': True},
    {'skip_text_preprocessing': False, 'use_stemming': False, 'use_lemmatization': True, 'keep_stopwords': False},
    {'skip_text_preprocessing': False, 'use_stemming': False, 'use_lemmatization': True, 'keep_stopwords': True},
]


######################################################################################
# Insert evaluations.
######################################################################################

with connection.cursor() as cursor:
    # Truncate our table.
    cursor.execute(truncate_sql)

    ######################################################################################
    # HDBSCAN.
    ######################################################################################

    min_cluster_sizes = [3, 4, 5, 6]
    metrics = ['cosine', 'euclidean']
    leaf_sizes = [20, 30, 40, 50, 60]
    allow_single_clusters = [True, False]

    for row in rows:
        for skip_rows in range(0, chunks):
            for preprocessing in preprocessings:
                for min_cluster_size in min_cluster_sizes:
                    for metric in metrics:
                        for leaf_size in leaf_sizes:
                            for allow_single_cluster in allow_single_clusters:
                                parameters = [
                                    '--rows=' + str(row),
                                    '--skip-rows=' + str(skip_rows),
                                    '--min-cluster-size=' + str(min_cluster_size),
                                    '--metric=' + str(metric),
                                    '--leaf-size=' + str(leaf_size),
                                ]

                                if preprocessing['skip_text_preprocessing']:
                                    parameters.append('--skip-text-preprocessing')
                                else:
                                    if preprocessing['use_stemming']:
                                        parameters.append('--use-stemming')
                                    elif preprocessing['use_lemmatization']:
                                        parameters.append('--use-lemmatization')

                                    if preprocessing['keep_stopwords']:
                                        parameters.append('--keep-stopwords')

                                if allow_single_cluster:
                                    parameters.append('--allow-single-cluster')

                                parameters = ' '.join(parameters)

                                cursor.execute(
                                    insert_sql,
                                    args=[
                                        'hdbscan',
                                        row,
                                        (skip_rows * row),
                                        None,
                                        None,
                                        parameters,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        0,
                                        None,
                                    ],
                                )

                                connection.commit()
    connection.close()
