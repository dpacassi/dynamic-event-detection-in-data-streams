import os
import pymysql
import pandas


def get_connection():
    return pymysql.connect(
        host=os.environ["MYSQL_HOSTNAME"],
        port=int(os.environ["MYSQL_PORT"]),
        user=os.environ["MYSQL_USER"],
        passwd=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


def get_last_script_execution(name):
    connection = get_connection()
    sql = (
        "SELECT *"
        " FROM script_execution"
        " WHERE script = %s AND failed = 0"
        " ORDER BY execution_date DESC"
    )

    data = pandas.read_sql(sql=sql, con=connection, index_col="id", params=[name])
    connection.close()

    return data


def add_script_execution(
    name, last_processed_date, failed, log_message, processing_time, result, new_rows, is_full_cluster, nrows
):
    connection = get_connection()

    insert_sql = (
        "INSERT INTO script_execution"
        " (script, last_processed_date, failed, log_message, processing_time, result, new_rows, is_full_cluster, nrows)"
        " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    with connection.cursor() as cursor:
        cursor.execute(
            insert_sql,
            args=[name, last_processed_date, failed, log_message, processing_time, result, new_rows, is_full_cluster, nrows],
        )

    connection.commit()
    connection.close()


def get_clusters():
    connection = get_connection()
    sql = "SELECT * FROM cluster WHERE method_evaluation_id is NULL ORDER BY id DESC"

    data = pandas.read_sql(sql=sql, con=connection, index_col="id")
    connection.close()

    return data


def add_cluster(identifier, method_id=None):
    connection = get_connection()

    insert_sql = "INSERT INTO cluster" " (identifier, method_evaluation_id)" " VALUES ( %s, %s )"

    insert_id = None
    with connection.cursor() as cursor:
        cursor.execute(insert_sql, args=[identifier, method_id])
        insert_id = cursor.lastrowid
        connection.commit()

    connection.close()
    return insert_id


def update_cluster(cluster_id, identifier):
    connection = get_connection()

    update_sql = "UPDATE cluster" " SET identifier = %s" " WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(update_sql, args=[identifier, cluster_id])

    connection.commit()
    connection.close()


def add_event(event_type, cluster_id, additional_information=""):
    connection = get_connection()

    insert_sql = "INSERT INTO event" " (type, cluster_id, additional_information)" " VALUES ( %s, %s, %s )"

    insert_id = None
    with connection.cursor() as cursor:
        cursor.execute(insert_sql, args=[event_type, cluster_id, additional_information])

        insert_id = cursor.lastrowid
        connection.commit()

    connection.close()
    return insert_id


def get_news_articles(nrows=1000, skip_rows=0):
    connection = get_connection()

    get_sql = (
        "SELECT *"
        " FROM news_article"
        " WHERE"
        "     newspaper_processed = 1"
        "     AND newspaper_text != ''"
        " ORDER BY date ASC"
        " LIMIT %s, %s"
    )

    data = pandas.read_sql(
        sql=get_sql, con=connection, index_col="id", params=[skip_rows, nrows]
    )
    connection.close()

    return data


def get_news_articles_from_date(date, nrows=1000, skip_rows=0):
    connection = get_connection()

    get_sql = (
        "SELECT *"
        " FROM news_article"
        " WHERE newspaper_processed = 1"
        "     AND title_keywords_intersection = 1"
        "     AND hostname != 'newsledge.com'"
        "     AND hostname != 'www.newsledge.com'"
        "     AND newspaper_text IS NOT NULL"
        "     AND TRIM(COALESCE(newspaper_text, '')) != ''"
        "     AND newspaper_text NOT LIKE '%%GDPR%%'"
        "     AND newspaper_text NOT LIKE '%%javascript%%'"
        "     AND newspaper_text NOT LIKE '%%404%%'"
        "     AND newspaper_text NOT LIKE '%%cookie%%'"
        "     AND date <= %s"
        " ORDER BY date DESC"
        " LIMIT %s, %s"
    )

    data = pandas.read_sql(
        sql=get_sql, con=connection, index_col="id", params=[date, skip_rows, nrows]
    )
    connection.close()

    return data


def add_news_to_cluster(cluster_id, news_article_id):
    connection = get_connection()

    insert_sql = (
        "INSERT INTO cluster_news_article"
        " (cluster_id, news_article_id)"
        " VALUES ( %s,  %s )"
    )

    with connection.cursor() as cursor:
        cursor.execute(insert_sql, args=[cluster_id, news_article_id])

    return connection.commit()


def get_news_id_by_cluster(news_ids):
    connection = get_connection()

    get_sql = "SELECT *" " FROM cluster_news_article" " WHERE news_article_id in (%s)"

    data = pandas.read_sql(sql=get_sql, con=connection, params=[news_ids])
    connection.close()

    return data


def write_failed_to_db(db_id):
    if db_id > 0:
        connection = get_connection()

        update_sql = "UPDATE cron_evaluation SET failed = 1 WHERE id = %s"

        with connection.cursor() as cursor:
            cursor.execute(update_sql, db_id)
            connection.commit()

        connection.close()


def write_preprocessing_time_to_db(db_id, preprocessing_time):
    if db_id > 0:
        connection = get_connection()

        update_sql = "UPDATE cron_evaluation SET time_preprocessing = %s WHERE id = %s"

        with connection.cursor() as cursor:
            cursor.execute(update_sql, ((preprocessing_time * 1000), db_id))
            connection.commit()

        connection.close()


def write_evaluation_result_in_db(
    method,
    sample_size,
    vectorizer,
    tokenizer,
    parameters,
    corrected_avg_unique_accuracy,
    avg_unique_accuracy,
    normalized_mutual_info_score,
    adjusted_mutual_info_score,
    completeness_score,
    estimated_clusters,
    real_clusters,
    n_noise,
    processing_time,
):
    connection = get_connection()

    insert_sql = (
        "INSERT INTO method_evaluation"
        " (method, sample_size, vectorizer, tokenizer, parameters, corrected_avg_unique_accuracy, avg_unique_accuracy, normalized_mutual_info_score, adjusted_mutual_info_score, completeness_score, estimated_clusters, real_clusters, n_noise, processing_time)"
        " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    insert_id = None
    with connection.cursor() as cursor:
        cursor.execute(
            insert_sql,
            args=[
                method,
                sample_size,
                vectorizer,
                tokenizer,
                parameters,
                corrected_avg_unique_accuracy,
                avg_unique_accuracy,
                normalized_mutual_info_score,
                adjusted_mutual_info_score,
                completeness_score,
                estimated_clusters,
                real_clusters,
                n_noise,
                processing_time,
            ],
        )
        insert_id = cursor.lastrowid
        connection.commit()

    connection.close()
    return insert_id


def load_news_by_ids(news_ids):
    connection = get_connection()
    id_str = ",".join(["'" + x + "'" for x in news_ids])

    news_sql = (
        "SELECT id, story"
        " FROM news_article"
        " WHERE id in ({}) ".format(id_str)
    )

    data = pandas.read_sql(sql=news_sql, con=connection)
    connection.close()
    return data


def reset_online_evaluation():
    connection = get_connection()

    sql = "DELETE from cluster where method_evaluation_id is null"

    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()

    sql = "TRUNCATE script_execution"

    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()


    connection.close()