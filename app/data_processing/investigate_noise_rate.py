import db
import pandas
import numpy as np
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
connection = db.get_connection()


sql = (
    "select additional_information from event"
    " join cluster on cluster.id = event.cluster_id"
    " where cluster.simulated_date is not null and  event.type = 2"
)

data = pandas.read_sql(sql=sql, con=connection)
count = 0

for index, row in data.iterrows():
    result = eval(row["additional_information"])
    count += len(result["additions"])

print(count / len(data))