import os
import pymysql
from dotenv import load_dotenv

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
chunks = 4


######################################################################################
# Insert evaluations.
######################################################################################

with connection.cursor() as cursor:
    # Truncate our table.
    cursor.execute(truncate_sql)

    ######################################################################################
    # HDBSCAN.
    ######################################################################################

    min_cluster_sizes = [2, 3, 4, 5, 6, 7]
    metrics = ['cosine', 'minkowski', 'euclidean']
    leaf_sizes = [10, 20, 30, 40, 50, 60, 70]
    allow_single_clusters = [True, False]

    for row in rows:
        for skip_rows in range(0, chunks):
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
