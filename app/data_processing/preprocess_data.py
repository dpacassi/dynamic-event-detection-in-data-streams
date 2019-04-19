import os
import time
import utils
import pymysql
from newspaper import Article
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

get_sql = (
    "SELECT *"
    " FROM news_article"
    " WHERE"
    "     newspaper_processed = 1"
    "     AND title_keywords_intersection = 1"
    "     AND hostname != 'newsledge.com'"
    "     AND hostname != 'www.newsledge.com'"
    "     AND newspaper_text IS NOT NULL"
    "     AND TRIM(COALESCE(newspaper_text, '')) != ''"
    "     AND newspaper_text NOT LIKE '%%GDPR%%'"
    "     AND newspaper_text NOT LIKE '%%javascript%%'"
    "     AND newspaper_text NOT LIKE '%%404%%'"
    "     AND newspaper_text NOT LIKE '%%cookie%%'"
    "     AND newspaper_keywords NOT LIKE '%%GDPR%%'"
    "     AND newspaper_keywords NOT LIKE '%%javascript%%'"
    "     AND newspaper_keywords NOT LIKE '%%404%%'"
    "     AND newspaper_keywords NOT LIKE '%%cookie%%'"
    "     AND preprocessed = 0"
    "     AND preprocessing_failed = 0"
    " ORDER BY id ASC"
    " LIMIT 1"
)

update_sql = (
    "UPDATE news_article"
    " SET newspaper_publish_date = %s,"
    " SET text_without_stopwords = %s,"
    " SET time_without_stopwords = %s,"
    " SET text_keyterms = %s,"
    " SET time_keyterms = %s,"
    " SET text_entities = %s,"
    " SET time_entities = %s,"
    " SET text_keyterms_and_entities = %s,"
    " SET time_keyterms_and_entities = %s,"
    " SET text_stemmed = %s,"
    " SET time_stemmed = %s,"
    " SET text_stemmed_without_stopwords = %s,"
    " SET time_stemmed_without_stopwords = %s,"
    " SET text_stemmed_without_stopwords_aggr = %s,"
    " SET time_stemmed_without_stopwords_aggr = %s,"
    " SET text_lemmatized = %s,"
    " SET time_lemmatized = %s,"
    " SET text_lemmatized_without_stopwords = %s,"
    " SET time_lemmatized_without_stopwords = %s,"
    " SET text_lemmatized_without_stopwords_aggr = %s,"
    " SET time_lemmatized_without_stopwords_aggr = %s,"
    " SET preprocessed = %s,"
    " SET preprocessing_failed = %s"
    " WHERE id = %s"
)


######################################################################################
# Preprocess texts.
######################################################################################

with connection.cursor() as cursor:
    cursor.execute(get_sql)
    rows = cursor.fetchall()

    for row in rows:
        article = Article(row['url'])
        article.download()
        article.parse()

        # Publish date.
        newspaper_publish_date = article.publish_date

        # Text without stopwords.
        start = time.time()
        text_without_stopwords = utils.f_remove_stopwords(row['newspaper_text'])
        end = time.time()
        time_without_stopwords = (end - start) * 1000

        text_keyterms = None
        time_keyterms = None
        text_entities = None
        time_entities = None
        text_keyterms_and_entities = None
        time_keyterms_and_entities = None
        text_stemmed = None
        time_stemmed = None
        text_stemmed_without_stopwords = None
        time_stemmed_without_stopwords = None
        text_stemmed_without_stopwords_aggr = None
        time_stemmed_without_stopwords_aggr = None
        text_lemmatized = None
        time_lemmatized = None
        text_lemmatized_without_stopwords = None
        time_lemmatized_without_stopwords = None
        text_lemmatized_without_stopwords_aggr = None
        time_lemmatized_without_stopwords_aggr = None
        preprocessed = None
        preprocessing_failed = None
