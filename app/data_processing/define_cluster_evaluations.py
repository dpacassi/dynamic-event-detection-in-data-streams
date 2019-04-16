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

truncate_sql = "TRUNCATE TABLE cron_evaluation"


with connection.cursor() as cursor:
    # Truncate our table.
    cursor.execute(truncate_sql)
    connection.close()
