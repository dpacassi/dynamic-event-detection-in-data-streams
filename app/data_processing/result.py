from sklearn.metrics import (
    completeness_score,
    homogeneity_score,
    v_measure_score,
    adjusted_rand_score,
    adjusted_mutual_info_score,
    silhouette_score,
)
from sklearn.metrics.cluster import normalized_mutual_info_score


class Result:
    def __init__(
        self,
        title,
        labels,
        processing_time,
        features=None,
        vectorizer=None,
        tokenizer=None,
        parameters=None,
    ):
        self.title = title
        self.labels = labels
        self.features = features
        self.parameters = parameters
        self.vectorizer = vectorizer
        self.tokenizer = tokenizer
        self.processing_time = processing_time

    def create_evaluation(self, y_true):
        # Number of clusters in labels, ignoring noise if present.
        return {
            "n_clusters": len(set(self.labels)) - (1 if -1 in self.labels else 0),
            "n_noise": list(self.labels).count(-1),
            "homogeneity_score": homogeneity_score(y_true, self.labels),
            "completeness_score": completeness_score(y_true, self.labels),
            "v_measure_score": v_measure_score(y_true, self.labels),
            "normalized_mutual_info_score": normalized_mutual_info_score(
                y_true, self.labels, average_method="arithmetic"
            ),
            "adjusted_rand_score": adjusted_rand_score(y_true, self.labels),
            "adjusted_mutual_info_score": adjusted_mutual_info_score(
                y_true, self.labels
            ),
        }

    def print_evaluation(self, y_true):
        scores = self.create_evaluation(y_true)
        print("------------------------------")
        print(self.title)
        print()
        print("Estimated number of clusters: %d" % scores["n_clusters"])
        print("Estimated number of noise points: %d" % scores["n_noise"])
        print("Homogeneity: %0.3f" % scores["homogeneity_score"])
        print("Completeness: %0.3f" % scores["completeness_score"])
        print("V-measure: %0.3f" % scores["v_measure_score"])
        print("NMI score: %0.3f" % scores["normalized_mutual_info_score"])
        print("Adjusted Rand Index: %0.3f" % scores["adjusted_rand_score"])
        print(
            "Adjusted Mutual Information: %0.3f" % scores["adjusted_mutual_info_score"]
        )
        print("Processing time: %0.2f seconds" % self.processing_time)
        print()

    def write_evaluation_to_db(self, y_true, db_id, time_total, real_clusters):
        scores = self.create_evaluation(y_true)
        connection = pymysql.connect(
            host=os.environ["MYSQL_HOSTNAME"],
            port=int(os.environ["MYSQL_PORT"]),
            user=os.environ["MYSQL_USER"],
            passwd=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        update_sql = "UPDATE cron_evaluation SET normalized_mutual_info_score = %s, adjusted_mutual_info_score = %s, completeness_score = %s, estimated_clusters = %s, real_clusters = %s, n_noise = %s, time_clustering = %s, time_total = %s, processed=1 WHERE id = %s"

        with connection.cursor() as cursor:
            s1 = float("{0:.8f}".format(scores['normalized_mutual_info_score']))
            s2 = float("{0:.8f}".format(scores['adjusted_mutual_info_score']))
            s3 = float("{0:.8f}".format(scores['completeness_score']))

            cursor.execute(update_sql, (s1, s2, s3, scores['n_clusters'], real_clusters, scores['n_noise'], (self.processing_time * 1000), (time_total * 1000), db_id))
            connection.commit()

        connection.close()
