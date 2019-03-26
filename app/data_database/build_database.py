import os
import csv
import pymysql
from datetime import datetime
from dotenv import load_dotenv

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

sql = "INSERT INTO news_article (id, title, url, publisher, category, story, hostname, date, newspaper_processed, newspaper_meta_language, newspaper_keywords, newspaper_text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
data = []

with open('data/uci-news-aggregator.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

    # Skip the header row.
    next(csv_reader, None)

    for row in csv_reader:
        data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], datetime.fromtimestamp(int(row[7])/1000), 0, None, None, None))

with connection.cursor() as cursor:
    cursor.executemany(sql, data)

connection.commit()
