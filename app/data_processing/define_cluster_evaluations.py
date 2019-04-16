import os
import argparse
import pymysql
import utils
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

# Check for command line arguments.
parser = argparse.ArgumentParser()

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
    " (method, rows, skip_rows, vectorizer, tokenizer, parameters, normalized_mutual_info_score, adjusted_mutual_info_score, completeness_score, estimated_clusters, real_clusters, n_noise, time_clustering, time_preprocessing, time_total, processed, failed)"
    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)

with connection.cursor() as cursor:
    # Truncate our table.
    cursor.execute(truncate_sql)
    connection.close()

    # Insert hdbscan calls.

