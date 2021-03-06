import os
import sys
import pymysql
import subprocess
from dotenv import load_dotenv
import cluster_evaluation

# Load environment variables.
load_dotenv()
script_names = ['cluster_evaluation_wrapper.py', 'cluster_evaluation.py']


######################################################################################
# Step 1: Check if the script is already running.
######################################################################################

for script_name in script_names:
    status = subprocess.getstatusoutput(
        "ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'| awk '{print $2}'" % script_name
    )
    if status[1]:
        sys.exit(0)

######################################################################################
# Step 2: Retrieve open evaluations from the database.
######################################################################################

connection = pymysql.connect(
    host=os.environ['MYSQL_HOSTNAME'],
    port=int(os.environ['MYSQL_PORT']),
    user=os.environ['MYSQL_USER'],
    passwd=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

get_sql = "SELECT * FROM cron_evaluation WHERE processed = 0 AND failed IS NULL ORDER BY id ASC"

with connection.cursor() as cursor:
    cursor.execute(get_sql)
    rows = cursor.fetchall()
    connection.close()

    for row in rows:
        args = [
            '--db-id=' + str(row['id']),
            '--method=' + str(row['method']),
            '--rows=' + str(row['rows']),
            '--skip-rows=' + str(row['skip_rows']),
        ] + row['parameters'].split()

        ######################################################################################
        # Step 3: Run cluster_evaluation.py with the defined arguments in the database.
        ######################################################################################

        cluster_evaluation.main(args)
