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
    name, last_processed_date, failed, log_message, processing_time
):
    connection = get_connection()

    insert_sql = (
        "INSERT INTO script_execution"
        " (script, last_processed_date, failed, log_message, processing_time)"
        " VALUES ( %s, %s, %s, %s, %s)"
    )

    with connection.cursor() as cursor:
        cursor.execute(
            insert_sql,
            args=[name, last_processed_date, failed, log_message, processing_time],
        )

    return connection.commit()


def get_clusters():
    connection = get_connection()
    sql = "SELECT * FROM cluster ORDER BY id DESC"

    data = pandas.read_sql(sql=sql, con=connection, index_col="id")
    connection.close()

    return data


def add_cluster(identifier):
    connection = get_connection()

    insert_sql = "INSERT INTO cluster" " (identifier)" " VALUES ( %s )"

    with connection.cursor() as cursor:
        cursor.execute(insert_sql, args=[identifier])

    connection.commit()
    return connection.insert_id()


def update_cluster(cluster_id, identifier):
    connection = get_connection()

    update_sql = "UPDATE cluster" " SET identifier = %s" " WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(update_sql, args=[identifier, cluster_id])

    return connection.commit()


def add_event(event_type, cluster_id, additional_information=""):
    connection = get_connection()

    insert_sql = "INSERT INTO event" " (type, cluster_id, additional_information)" " VALUES ( %s, %s, %s )"

    with connection.cursor() as cursor:
        cursor.execute(insert_sql, args=[event_type, cluster_id, additional_information])

    return connection.commit()


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
        " WHERE"
        "     newspaper_processed = 1"
        "     AND newspaper_text != ''"
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
