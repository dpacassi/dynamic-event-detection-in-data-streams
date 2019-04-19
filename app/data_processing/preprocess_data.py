import os
import pymysql
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

# Get news articles to preprocess.
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

######################################################################################
# Preprocess texts.
######################################################################################

with connection.cursor() as cursor:
    cursor.execute(get_sql)
    rows = cursor.fetchall()

    for row in rows:
        row = row