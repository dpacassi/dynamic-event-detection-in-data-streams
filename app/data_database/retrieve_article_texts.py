import os
import argparse
import pymysql
from newspaper import Article
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

# Check for command line arguments.
parser = argparse.ArgumentParser()

parser.add_argument('--limit', default=10000, help='How many news articles to process.')
parser.add_argument('--from', default=0, help='Starting ID from news articles to process.')
parser.add_argument('--to', default=1000000, help='Ending ID from news articles to process.')

args = parser.parse_args()
limit = 10000
if isinstance(getattr(args, 'limit'), int):
    limit = getattr(args, 'limit')
elif getattr(args, 'limit').isdigit():
    limit = int(getattr(args, 'limit'))

from_id = 0
if isinstance(getattr(args, 'from'), int):
    from_id = getattr(args, 'from')
elif getattr(args, 'from') is not None and getattr(args, 'from').isdigit():
    from_id = int(getattr(args, 'from'))

to_id = 1000000
if isinstance(getattr(args, 'to'), int):
    to_id = getattr(args, 'to')
elif getattr(args, 'to') is not None and getattr(args, 'to').isdigit():
    to_id = int(getattr(args, 'to'))

connection = pymysql.connect(
    host=os.environ['MYSQL_HOSTNAME'],
    port=int(os.environ['MYSQL_PORT']),
    user=os.environ['MYSQL_USER'],
    passwd=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

get_sql = "SELECT * FROM news_article WHERE newspaper_processed = 0 AND id >= %s AND id <= %s ORDER BY id ASC LIMIT %s"
update_sql = "UPDATE news_article SET newspaper_processed = 1, newspaper_meta_language = %s, newspaper_keywords = %s, newspaper_text = %s WHERE id = %s"

with connection.cursor() as cursor:
    cursor.execute(get_sql, (from_id, to_id, limit))
    rows = cursor.fetchall()

    for row in rows:
        news_article = Article(row["url"])
        news_language = None
        news_keywords = None
        news_text = None

        try:
            news_article.download()
            news_article.parse()
            news_article.nlp()
            news_language = news_article.meta_lang
            news_keywords = ",".join(news_article.keywords)
            news_text = news_article.text

            if not news_language:
                news_language = None
        except:
            news_language = None
            news_keywords = None
            news_text = None

        cursor.execute(update_sql, (news_language, news_keywords, news_text, row["id"]))
        connection.commit()
