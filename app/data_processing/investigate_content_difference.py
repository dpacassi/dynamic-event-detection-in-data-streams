import db
import pandas
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
connection = db.get_connection()

n_articles = 10

story = 'd2_970npmWUODiMcylX3Bo3yrz0_M'
method_evaluation = 4368

sql = (
    "select title, newspaper_text, story, cluster.id, publisher from news_article"
    " join cluster_news_article on news_article.id = cluster_news_article.news_article_id"
    " join cluster on cluster.id = cluster_news_article.cluster_id"
    " where method_evaluation_id = %s and story = %s"
)

detected_articles = pandas.read_sql(sql=sql, con=connection, params=[method_evaluation, story])

sql = (
    "select title, newspaper_text, story, publisher from news_article"
    " where id not in ("
    "	select  news_article.id from news_article"
    "	join cluster_news_article on news_article.id = cluster_news_article.news_article_id"
    "	join cluster on cluster.id = cluster_news_article.cluster_id"
    "	where method_evaluation_id = %s)"
    " and story = %s"
    " and preprocessed = 1;"
)

missed_articles = pandas.read_sql(sql=sql, con=connection, params=[method_evaluation, story])
detected_table = []
missed_table = []

headlines = []

i = 1
for index, row in detected_articles[:n_articles].iterrows():
    detected_table.append(row["newspaper_text"])
    headlines.append(row["title"])
    i += 1

for index, row in missed_articles[:n_articles].iterrows():
    missed_table.append(row["newspaper_text"])
    headlines.append(row["title"])
    i += 1

all_articles = detected_table + missed_table

vectorizer = TfidfVectorizer(
    min_df=3, max_df=0.9, lowercase=True, analyzer="word", stop_words="english"
)


matrix = vectorizer.fit_transform(all_articles)
features = vectorizer.get_feature_names()

print(features[90])

table = []

for i, row in enumerate(matrix):
    features_per_article = []

    dense_row = np.squeeze(np.asarray(row.todense()))

    for j, value in enumerate(dense_row):
        features_per_article.append((features[j], value))

    features_per_article.sort(key=lambda x: x[1], reverse=True)

    top_10 = [x[0] for x in features_per_article[:10]]
    print("Nr. {}: {}".format(i, top_10))

    table.append([i + 1, top_10])


latex = tabulate(table, headers=["Nr.", "Top 10 Keywords"], tablefmt="latex")
print(latex)
    