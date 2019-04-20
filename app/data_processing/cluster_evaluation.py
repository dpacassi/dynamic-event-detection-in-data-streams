import collections
import argparse
import time
import math

from dotenv import load_dotenv

from hdbscan import HDBSCAN

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

import utils


class ClusterEvaluation:
    def __init__(self, documents, full_dataset=None):
        self.documents = documents
        self.full_dataset = full_dataset
        self.data_matrix = []
        self.excluded_entity_types = ["CARDINAL", "ORDINAL", "QUANTITY"]

    ############################

    # K-Means:
    # We use kmeans as a baseline to evaluate the hdbscan method
    #
    # Since kmeans needs a fixed number of clusters as input, we use the elbow
    # method to find an usable approximate of the total number of clusters. The
    # starting point is calculated based on the square root of number of documents.

    def kmeans(self, n_range=1):
        n_approx = int(math.sqrt(len(self.documents)))
        n_range = 1
        n_start = n_approx - n_range
        n_end = n_approx + n_range

        distances = []

        start = time.time()

        K = range(n_start, n_end)
        for k in K:
            model = KMeans(n_clusters=k).fit(self.data_matrix)
            distances.append(model.inertia_)
            labels = model.predict(self.data_matrix)

        end = time.time()

        return labels, (end - start)

    ############################

    # HDBSCAN:
    # We use a simple count matrix and cluster it using hdbscan.
    #
    # The reasoning for hdbscan is, that we don't have a fixed number of clusters, since it
    # depends on the given samples. Hdbscan solves this issue by not requiring a fixed number
    # of clusters beforehand as opposed to kmeans. Additionally hdbscan is supposed to solve
    # the issues regarding clusters of varying density of its predecessor dbscan.

    def hdbscan(self, args):
        start = time.time()
        model = HDBSCAN(
            min_cluster_size=args["min_cluster_size"],
            metric=args["metric"],
            leaf_size=args["leaf_size"],
            allow_single_cluster=args["allow_single_cluster"],
        ).fit(self.data_matrix)
        labels = model.predict(self.data_matrix)
        end = time.time()
        return labels, (end - start)

    def create_data_matrix(self, vectorizer):
        vectorizer = CountVectorizer(
            min_df=3, max_df=0.9, lowercase=True, analyzer="word", stop_words="english"
        ).fit(self.documents)

        self.data_matrix = vectorizer.transform(self.documents)
        features = vectorizer.get_feature_names()

        # Extract entities from sparse data_matrix
        self.features_by_document = utils.map_features_to_word_vectors(
            self.data_matrix, features
        )

    def run(self, methods, args):
        # Run clusterings
        results = []
        vectorizer = None

        if args["vectorizer"] == "count":
            vectorizer = CountVectorizer(
                min_df=args["min_df"],
                max_df=args["max_df"],
                lowercase=True,
                analyzer="word",
                stop_words="english",
            )
        elif args["vectorizer"] == "tfidf":
            vectorizer = TfidfVectorizer(
                min_df=args["min_df"],
                max_df=args["max_df"],
                lowercase=True,
                analyzer="word",
                stop_words="english",
            )

        self.create_data_matrix(vectorizer)

        if "kmeans" in methods:
            labels, processing_time = self.kmeans()
            results.append(utils.Result("KMeans", labels, processing_time))

        if "hdbscan" in methods:
            labels, processing_time = self.hdbscan(args)
            results.append(utils.Result("HDBSCAN", labels, processing_time))
        return results


def main(passed_args=None):
    # Note: Download nlp datasets the first time you run this script.
    # python -m spacy download en_core_web_md
    # python -m gensim.downloader --download fasttext-wiki-news-subwords-300

    # Load environment variables.
    load_dotenv()

    # Handle arguments.
    ap = argparse.ArgumentParser()
    ap.add_argument("--methods", required=False, type=str, default="hdbscan_entities")
    ap.add_argument("--rows", required=False, type=int, default=1000)
    ap.add_argument("--skip-rows", required=False, type=int, default=0)
    ap.add_argument("--source", required=False, type=str, default="database")
    ap.add_argument("--vectorizer", required=False, type=str, default="count")
    ap.add_argument("--tokenizer", required=False, type=str, default="extract_entities")
    ap.add_argument("--min-df", required=False, type=float, default=3)
    ap.add_argument("--max-df", required=False, type=float, default=0.9)
    ap.add_argument("--min-cluster-size", required=False, type=int, default=3)
    ap.add_argument("--leaf-size", required=False, type=int, default=40)
    ap.add_argument("--db-id", required=False, type=int, default=0)
    ap.add_argument("--metric", required=False, type=str, default="euclidean")
    ap.add_argument("--verbosity", required=False, type=int, default=0)
    ap.add_argument(
        "--skip-text-preprocessing", dest="skip_text_preprocessing", action="store_true"
    )
    ap.set_defaults(skip_text_preprocessing=False)
    ap.add_argument("--keep-stopwords", dest="keep_stopwords", action="store_true")
    ap.set_defaults(keep_stopwords=False)
    ap.add_argument("--use-stemming", dest="use_stemming", action="store_true")
    ap.set_defaults(use_stemming=False)
    ap.add_argument(
        "--use-lemmatization", dest="use_lemmatization", action="store_true"
    )
    ap.set_defaults(use_lemmatization=False)
    ap.add_argument(
        "--allow-single-cluster", dest="allow_single_cluster", action="store_true"
    )
    ap.set_defaults(allow_single_cluster=False)

    if passed_args is not None:
        args = vars(ap.parse_args(passed_args))
    else:
        args = vars(ap.parse_args())

    # Load data and setup for evaluation
    id_column = "id"
    content_column = "newspaper_text"
    headline_column = "title"
    story_column = "story"
    start = time.time()

    if args["source"] == "csv":
        dataset = utils.load_test_data(
            nrows=args["rows"],
            skip_rows=args["skip_rows"],
            skip_text_preprocessing=args["skip_text_preprocessing"],
            keep_stopwords=args["keep_stopwords"],
            use_stemming=args["use_stemming"],
            use_lemmatization=args["use_lemmatization"],
            db_id=args["db_id"],
        )
    else:
        dataset = utils.load_test_data_from_db(
            nrows=args["rows"],
            skip_rows=args["skip_rows"],
            skip_text_preprocessing=args["skip_text_preprocessing"],
            keep_stopwords=args["keep_stopwords"],
            use_stemming=args["use_stemming"],
            use_lemmatization=args["use_lemmatization"],
            db_id=args["db_id"],
        )

    try:
        labels_true = LabelEncoder().fit_transform(dataset[story_column])
        results = ClusterEvaluation(dataset[content_column], dataset).run(
            args["methods"].split(","), args
        )
        end = time.time()
    except BaseException as e:
        print("Error:")
        print(e)
        results = []
        if args["db_id"] > 0:
            utils.write_failed_to_db(args["db_id"])

    if args["verbosity"] >= 1:
        print("True number of clusters: %d" % len(set(labels_true)))
        print("")

    # Print resultsdataset
    for result in results:
        if args["verbosity"] >= 1:
            result.print_evaluation(labels_true)

        if args["verbosity"] >= 2 and result.features is not None:
            print(len(result.features))
            grouped_indices = collections.defaultdict(list)
            for index, value in enumerate(result.labels):
                if value >= 0:
                    grouped_indices[value].append(index)

            for key, indices in grouped_indices.items():
                print("Group %d: \n" % key)
                # print(indices)
                for index in indices:
                    print(
                        "{}: {}".format(
                            dataset[id_column][index], dataset[headline_column][index]
                        )
                    )
                    # print("Entities: {}".format(result.features[index] if index < len(result.features) else "no entities"))
                print("------------------------------")

            print(result.labels)
            print(result.n_topics)

        if args["db_id"] > 0:
            result.write_evaluation_to_db(
                labels_true, args["db_id"], (end - start), len(set(labels_true))
            )


if __name__ == "__main__":
    main()
