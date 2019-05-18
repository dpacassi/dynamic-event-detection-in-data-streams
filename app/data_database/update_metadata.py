import os
import random
import pymysql
import datetime
from dotenv import load_dotenv
from filelock import Timeout, FileLock

######################################################################################
# Check if the script is already running.
######################################################################################

ts = str(datetime.datetime.now())

try:
    lock = FileLock("metadata.lock", timeout=1)
    with lock:
        print("[" + ts + "] Received lock, updating metadata")

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

        # Get the next story to process.
        get_next_sql = "SELECT * FROM news_article WHERE preprocessed = 1 AND valid_story_count IS NULL LIMIT 1"
        get_stories_sql = "SELECT * FROM news_article WHERE preprocessed = 1 AND story = %s ORDER BY `date` ASC"
        update_story_sql = "UPDATE news_article SET valid_story_count = %s, computed_publish_date = %s WHERE id = %s"

        with connection.cursor() as cursor:
            while True:
                cursor.execute(get_next_sql)
                rows = cursor.fetchall()

                if len(rows) == 0:
                    break

                story = rows[0]['story']
                cursor.execute(get_stories_sql, (story))
                rows = cursor.fetchall()
                valid_story_count = len(rows)
                date = None

                for idx, news_article in enumerate(rows):
                    if idx > 0:
                        minutes_to_add = random.randint(1, 120)
                        seconds_to_add = random.randint(0, 59)
                        date += datetime.timedelta(minutes=minutes_to_add, seconds=seconds_to_add)
                    else:
                        date = news_article['date']

                    cursor.execute(update_story_sql, (valid_story_count, date, news_article['id']))
                    connection.commit()

        print("[" + ts + "] No stories to process")
        connection.close()
        lock.release()
except Timeout:
    print("[" + ts + "] Didn't receive lock")
