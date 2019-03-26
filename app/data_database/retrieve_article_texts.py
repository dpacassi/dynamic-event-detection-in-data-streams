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

        try:
            news_article.download()
            news_article.parse()
            news_article.nlp()
            keywords = ",".join(news_article.keywords)
            cursor.execute(update_sql, (news_article.meta_lang, keywords, news_article.text, row["id"]))
        except:
            cursor.execute(update_sql, (None, None, None, row["id"]))

connection.commit()
