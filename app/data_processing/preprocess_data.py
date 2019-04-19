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
)

update_sql = (
    "UPDATE news_article SET"
    " newspaper_publish_date = %s,"
    " text_without_stopwords = %s,"
    " time_without_stopwords = %s,"
    " text_keyterms = %s,"
    " time_keyterms = %s,"
    " text_entities = %s,"
    " time_entities = %s,"
    " text_keyterms_and_entities = %s,"
    " time_keyterms_and_entities = %s,"
    " text_stemmed = %s,"
    " time_stemmed = %s,"
    " text_stemmed_without_stopwords = %s,"
    " time_stemmed_without_stopwords = %s,"
    " text_stemmed_without_stopwords_aggr = %s,"
    " time_stemmed_without_stopwords_aggr = %s,"
    " text_lemmatized = %s,"
    " time_lemmatized = %s,"
    " text_lemmatized_without_stopwords = %s,"
    " time_lemmatized_without_stopwords = %s,"
    " text_lemmatized_without_stopwords_aggr = %s,"
    " time_lemmatized_without_stopwords_aggr = %s,"
    " preprocessed = 1,"
    " preprocessing_failed = 0"
    " WHERE id = %s"
)

update_failed_sql = (
    "UPDATE news_article SET"
    " preprocessed = 0,"
    " preprocessing_failed = 1"
    " WHERE id = %s"
)


######################################################################################
# Preprocess texts.
######################################################################################

with connection.cursor() as cursor:
    cursor.execute(get_sql)
    rows = cursor.fetchall()

    for row in rows:
        try:
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

            # Text keyterms.
            start = time.time()
            text_keyterms_list = utils.extract_keyterms(row['newspaper_text'])
            text_keyterms = ",".join(text_keyterms_list)
            end = time.time()
            time_keyterms = (end - start) * 1000

            # Text entities.
            start = time.time()
            text_entities_list = utils.extract_entities(row['newspaper_text'])
            text_entities = ",".join(text_entities_list)
            end = time.time()
            time_entities = (end - start) * 1000

            # Text keyterms and entities.
            text_keyterms_and_entities_list = text_keyterms_list + text_entities_list
            text_keyterms_and_entities_list = list(dict.fromkeys(text_keyterms_and_entities_list))
            text_keyterms_and_entities = ",".join(text_keyterms_and_entities_list)
            time_keyterms_and_entities = time_keyterms + time_entities

            # Text stemming.
            start = time.time()
            text_stemmed = utils.stem_text(row['newspaper_text'], False)
            end = time.time()
            time_stemmed = (end - start) * 1000

            # Text stemming without stopwords.
            start = time.time()
            text_stemmed_without_stopwords = utils.stem_text(row['newspaper_text'], True)
            end = time.time()
            time_stemmed_without_stopwords = (end - start) * 1000

            # Text stemming without stopwords and aggressive cleaning.
            start = time.time()
            text_stemmed_without_stopwords_aggr = utils.clean_text(row['newspaper_text'], keep_stopwords=False, use_stemming=True, use_lemmatization=False)
            end = time.time()
            time_stemmed_without_stopwords_aggr = (end - start) * 1000

            # Text lemmatization.
            start = time.time()
            text_lemmatized = utils.lemmatize_text(row['newspaper_text'], False)
            end = time.time()
            time_lemmatized = (end - start) * 1000

            # Text lemmatization without stopwords.
            start = time.time()
            text_lemmatized_without_stopwords = utils.lemmatize_text(row['newspaper_text'], True)
            end = time.time()
            time_lemmatized_without_stopwords = (end - start) * 1000

            # Text lemmatization without stopwords and aggressive cleaning.
            start = time.time()
            text_lemmatized_without_stopwords_aggr = utils.clean_text(row['newspaper_text'], keep_stopwords=False, use_stemming=False, use_lemmatization=True)
            end = time.time()
            time_lemmatized_without_stopwords_aggr = (end - start) * 1000

            # Write to database.
            cursor.execute(update_sql, (
                newspaper_publish_date,
                text_without_stopwords,
                time_without_stopwords,
                text_keyterms,
                time_keyterms,
                text_entities,
                time_entities,
                text_keyterms_and_entities,
                time_keyterms_and_entities,
                text_stemmed,
                time_stemmed,
                text_stemmed_without_stopwords,
                time_stemmed_without_stopwords,
                text_stemmed_without_stopwords_aggr,
                time_stemmed_without_stopwords_aggr,
                text_lemmatized,
                time_lemmatized,
                text_lemmatized_without_stopwords,
                time_lemmatized_without_stopwords,
                text_lemmatized_without_stopwords_aggr,
                time_lemmatized_without_stopwords_aggr,
                row["id"])
            )
            connection.commit()
        except:
            # Write to database.
            cursor.execute(update_failed_sql, (row["id"]))
            connection.commit()
