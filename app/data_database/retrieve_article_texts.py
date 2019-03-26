import os
import pymysql
from newspaper import Article
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

get_sql = "SELECT * FROM news_article WHERE newspaper_processed = 0 ORDER BY id ASC LIMIT 10000"
update_sql = "UPDATE news_article SET newspaper_processed = 1, newspaper_meta_language = %s, newspaper_keywords = %s, newspaper_text = %s WHERE id = %s"

with connection.cursor() as cursor:
    cursor.execute(get_sql)
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
