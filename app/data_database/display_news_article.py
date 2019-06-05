import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

# dzPKSNdo57BhoZM--2ed-Q4okkjaM
# dtaPXb6KyT2GPnMor6iUbM208BgmM
# dSW8j0C01F61QpMNttOVAPhLcNWLM

#story = 'dtaPXb6KyT2GPnMor6iUbM208BgmM'
story = None
id = 211128

get_sql_story = "SELECT * FROM news_article WHERE preprocessed = 1 AND story = %s ORDER BY id ASC LIMIT 100"
get_sql_id = "SELECT * FROM news_article WHERE id = %s"

connection = pymysql.connect(
    host=os.environ['MYSQL_HOSTNAME'],
    port=int(os.environ['MYSQL_PORT']),
    user=os.environ['MYSQL_USER'],
    passwd=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

with connection.cursor() as cursor:
    if story is not None:
        cursor.execute(get_sql_story, (story))
    else:
        cursor.execute(get_sql_id, (id))

    rows = cursor.fetchall()

    for row in rows:
        print(row['id'])
        print(row['title'])
        print(row['url'])
        print('')
        print('----- newspaper_text:')
        print(row['newspaper_text'])
        print('')
        print('----- text_keyterms:')
        print(row['text_keyterms'])
        print('length: ' + str(len(row['text_keyterms'].split(','))))
        print('')
        print('----- text_entities:')
        print(row['text_entities'])
        print('length: ' + str(len(row['text_entities'].split(','))))
        print('')
        print('----- text_stemmed_without_stopwords:')
        print(row['text_stemmed_without_stopwords'].lower())
        print('')
        print('----- text_lemmatized_without_stopwords:')
        print(row['text_lemmatized_without_stopwords'].lower())

    cursor.close()

connection.close()
