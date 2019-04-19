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
get_sql = 'SELECT * FROM news_article WHERE preprocessed = 0 AND failed IS NULL ORDER BY id ASC'