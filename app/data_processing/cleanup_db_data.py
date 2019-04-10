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

get_sql = "SELECT * FROM news_article WHERE title_keywords_intersection IS NULL ORDER BY id ASC"
update_sql = "UPDATE news_article SET title_keywords_intersection = %s WHERE id = %s"

with connection.cursor() as cursor:
    cursor.execute(get_sql)
    rows = cursor.fetchall()

    for row in rows:
        intersects = 0

        if row['newspaper_keywords'] is not None:
            keywords_content = set(row['newspaper_keywords'].split(','))

            keywords_title = row['title'].lower()
            keywords_title = utils.remove_punctuation(keywords_title)
            keywords_title = set(keywords_title.split())

            if keywords_content.intersection(keywords_title):
                intersects = 1

        cursor.execute(update_sql, (intersects, row['id']))
        connection.commit()
