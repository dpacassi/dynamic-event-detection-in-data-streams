# External modules
import time
import argparse
import json
import math
import numpy as np
import gc

from datetime import datetime
from itertools import chain
from dotenv import load_dotenv
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import (
    Birch,
    AffinityPropagation,
    MeanShift,
    SpectralClustering,
    KMeans,
)

# Internal modules
import db
import utils
import test_data
import score

from result import Result


class ClusterMethods:
    def __init__(self, documents, number_of_clusters, labels_true, document_ids):
        self.documents = documents
        self.labels_true = labels_true
        self.number_of_clusters = number_of_clusters
        self.nrows = len(documents)
        self.error_log = "error.log"
        self.document_ids = document_ids

    def hdbscan(self, data_matrix, **parameters):
        start = time.time()
        labels = HDBSCAN(**parameters).fit_predict(data_matrix)
        end = time.time()
        return labels, (end - start)

    def meanshift(self, data_matrix, **parameters):
        start = time.time()
        labels = MeanShift(**parameters).fit_predict(data_matrix.toarray())
        end = time.time()
        return labels, (end - start)

    def birch(self, data_matrix, **parameters):
        # https://scikit-learn.org/stable/modules/clustering.html#birch
        start = time.time()
        labels = Birch(n_clusters=None, **parameters).fit_predict(data_matrix)
        end = time.time()
        return labels, (end - start)

    def spectral_clustering(self, data_matrix, **parameters):
        start = time.time()
        labels = SpectralClustering(**parameters).fit_predict(data_matrix)
        end = time.time()
        return labels, (end - start)

    def affinity_propagation(self, data_matrix, **parameters):
        start = time.time()
        labels = AffinityPropagation(
            preference=None, verbose=False, **parameters
        ).fit_predict(data_matrix)
        end = time.time()
        return labels, (end - start)

    def hdbscan_lda(self, data_matrix, **parameters):
        start = time.time()
        hdbscan_labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(
            data_matrix
        )

        n_estimated_topics = len(set(hdbscan_labels)) - (
            1 if -1 in hdbscan_labels else 0
        )
        model = LatentDirichletAllocation(
            n_components=n_estimated_topics, **parameters
        ).fit(data_matrix)
        document_matrix = model.transform(data_matrix)

        lda_labels, documents_by_topic = utils.get_labels_and_documents_from_distribution_matrix(
            document_matrix, self.documents
        )
        end = time.time()

        return lda_labels, (end - start)

    def kmeans(self, data_matrix, **parameters):
        n_clusters = 0

        if parameters["n_cluster"] == "n_square":
            n_clusters = int(math.sqrt(len(self.documents)))
        if parameters["n_cluster"] == "n_true":
            n_clusters = self.number_of_clusters

        start = time.time()

        km = KMeans(n_clusters=n_clusters).fit(data_matrix)
        labels = km.predict(data_matrix)

        end = time.time()
        return labels, (end - start)

    def setup_evaluation(self):
        vectorizers = [
            CountVectorizer(
                min_df=3,
                max_df=0.9,
                lowercase=True,
                analyzer="word",
                stop_words="english",
                max_features=50000,
                dtype=np.int16,
            ),
            TfidfVectorizer(
                min_df=3,
                max_df=0.9,
                lowercase=True,
                analyzer="word",
                stop_words="english",
                max_features=50000,
            ),
        ]

        tokenizers = [
            None,
            # extract_entities,
            # extract_keyterms_and_entities,
            # TODO word2vec
        ]

        # Parameter arguments have to be a list
        parameters_by_method = {
            self.kmeans: {
                "n_cluster": ["n_true"],
                # ["n_square", "n_true"]
            },
            self.hdbscan: {
                # "min_cluster_size": [6],
                "min_cluster_size": range(2, 10),
                # "metric": ["cosine"]
                "metric": ["cosine", "euclidean"]
                # "metric": ["cosine", "manhattan", "euclidean"]
            },
            self.meanshift: {"cluster_all": [True, False]},
            self.birch: {
                "branching_factor": range(10, 100, 10),
                # "threshold": range(2, 6),
            },
            self.affinity_propagation: {
                "affinity": ["euclidean"],
                "convergence_iter": [15],
                "damping": np.arange(0.5, 0.9, 0.1),
                "max_iter": [50, 100, 200, 500],
            },
            self.spectral_clustering: {
                "affinity": ["rbf"],
                "assign_labels": ["kmeans", "discretize"],
            },
            # sself.hdbscan_lda: {"max_iter": [50, 100, 200, 500]},
        }

        return vectorizers, tokenizers, parameters_by_method

    def run(self, methods, whitelist_vectorizer, external_tokenizer):
        vectorizers, tokenizers, parameters_by_method = self.setup_evaluation()
        results = []
        errors = []

        for vectorizer in vectorizers:
            if (
                len(whitelist_vectorizer) > 0
                and vectorizer.__class__.__name__ not in whitelist_vectorizer
            ):
                continue

            for tokenizer in tokenizers:
                print(
                    "Use vectorizer {} with tokenizer {}".format(
                        vectorizer.__class__.__name__,
                        "None" if tokenizer is None else tokenizer.__name__,
                    )
                )

                if tokenizer is None:
                    vectorizer.set_params(tokenizer=tokenizer)

                data_matrix = vectorizer.fit_transform(self.documents)

                for method, parameters in parameters_by_method.items():
                    if len(methods) > 0 and method.__name__ not in methods:
                        continue

                    keys = list(parameters.keys())
                    values = list(parameters.values())
                    parameter_combinations = self.extract_parameters(
                        keys, values, {}, 0
                    )

                    # Flatten combinations to only have a one dimensional list
                    while isinstance(parameter_combinations[0], list):
                        parameter_combinations = list(
                            chain.from_iterable(parameter_combinations)
                        )

                    for parameter_combination in parameter_combinations:
                        print(
                            "Run method {} with parameters {}".format(
                                method.__name__, str(parameter_combination)
                            )
                        )
                        try:
                            labels, processing_time = method(
                                data_matrix, **parameter_combination
                            )

                            mp_score = self.calculate_cluster_accuracy(
                                labels, self.labels_true
                            )
                            method_id = self.store_result_to_db(
                                Result(
                                    method.__name__,
                                    labels,
                                    processing_time,
                                    None,
                                    vectorizer.__class__.__name__,
                                    external_tokenizer, # "None" if tokenizer is None else tokenizer.__name__,
                                    parameter_combination,
                                ),
                                mp_score
                            )

                            self.create_clusters(method_id, labels)

                        except BaseException as error:
                            error_message = "{} - {} while running {}: Message {}; Vectorizer {}; Tokenizer {}; Parameters {}; Nrows {};\n".format(
                                datetime.now(),
                                error.__class__.__name__,
                                method.__name__,
                                error,
                                vectorizer.__class__.__name__,
                                external_tokenizer, # "None" if tokenizer is None else tokenizer.__name__,
                                str(parameter_combination),
                                self.nrows,
                            )

                            errors.append(error_message)
                            with open(self.error_log, "a+") as log_file:
                                log_file.write(error_message)

        return errors

    def store_result_to_db(
        self, result, mp_score
    ):
        scores = result.create_evaluation(self.labels_true)
        return db.write_evaluation_result_in_db(
            str(result.title),
            int(self.nrows),
            str(result.vectorizer),
            str(result.tokenizer),
            str(json.dumps(result.parameters)),
            float(mp_score),
            float(scores["normalized_mutual_info_score"]),
            float(scores["completeness_score"]),
            float(scores["adjusted_mutual_info_score"]),
            int(scores["n_clusters"]),
            int(self.number_of_clusters),
            int(scores["n_noise"]),
            float(result.processing_time),
        )

    def calculate_cluster_accuracy(self, labels, labels_true):
        cluster_identifiers = utils.convert_labels_to_cluster_identifier(
            labels, self.document_ids
        )
        true_identifiers = utils.convert_labels_to_cluster_identifier(
            labels_true, self.document_ids
        )

        true_clusters = [
            true_identifier.split(",") for true_identifier in true_identifiers
        ]
        predicted_clusters = [
            cluster_identifier.split(",") for cluster_identifier in cluster_identifiers
        ]
        mp_score = score.calculate_mp_score(
            true_clusters, predicted_clusters
        )

        return mp_score

    def create_clusters(self, method_id, labels):
        cluster_identifiers = utils.convert_labels_to_cluster_identifier(
            labels, self.document_ids
        )
        for identifier in cluster_identifiers:
            cluster_id = db.add_cluster(identifier, method_id)
            document_ids = identifier.split(",")
            for document_id in document_ids:
                db.add_news_to_cluster(cluster_id, document_id)

    def extract_parameters(self, keys, values, param_chain, i):
        key = keys[i]
        parameter_combinations = []
        for value in values[i]:
            param_chain[key] = value
            new_chain = (
                self.extract_parameters(keys, values, param_chain, i + 1)
                if i < len(keys) - 1
                else param_chain
            )
            parameter_combinations.append(new_chain.copy())

        return parameter_combinations


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--rows", required=False, type=int, default=1000)
    ap.add_argument("--stories", required=False, type=str, default=None)
    ap.add_argument("--methods", required=False, type=str, default=None)
    ap.add_argument("--vectorizers", required=False, type=str, default=None, help="Options: CountVectorizer, TfidfVectorizer")
    ap.add_argument(
        "--tokenizers",
        required=False,
        type=str,
        default=None,
        help="Options: newspaper_text, text_keyterms, text_entities, text_keyterms_and_entities, text_lemmatized_without_stopwords, text_stemmed_without_stopwords",
    )
    ap.add_argument("--runs", required=False, type=int, default=1)
    args = vars(ap.parse_args())

    number_of_runs = args["runs"]
    nrows = args["rows"]
    methods = args["methods"].split(",") if args["methods"] is not None else list()
    tokenizers = (
        args["tokenizers"].split(",")
        if args["tokenizers"] is not None
        else ["newspaper_text"]
    )
    vectorizers = (
        args["vectorizers"].split(",") if args["vectorizers"] is not None else list()
    )
    story_runs = (
        map(int, args["stories"].split(",")) if args["stories"] is not None else [0]
    )

    load_dotenv()

    start = time.time()

    for nstories in story_runs:
        print("Use {} stories".format(nstories))
        for run in range(number_of_runs):
            print("Start run {}".format(run))

            if nstories > 0:
                dataset = test_data.load_from_db_by_stories(
                    nstories=nstories, skip_stories=run * nstories
                )
            else:
                dataset = test_data.load_from_db(nrows=nrows, skip_rows=run * nrows)

            labels_true = LabelEncoder().fit_transform(dataset["story"])
            stories_in_dataset = len(set(labels_true)) - (1 if -1 in labels_true else 0)

            errors = []
            for tokenizer in tokenizers:
                print("Use ", tokenizer)

                evaluation = ClusterMethods(
                    dataset[tokenizer],
                    stories_in_dataset,
                    labels_true,
                    list(dataset.index.values),
                )

                # delete full dataframe before evaluation to save some memory
                # del dataset
                # gc.collect()

                errors = evaluation.run(methods, vectorizers, tokenizer)

            if len(errors) > 0:
                print("Errors:")
                print(errors)
            print("Finished run {} with {} errors.".format(run, len(errors)))

    end = time.time()
    runtime = end - start
    print("Finished Evaluation after {}s.".format(len(errors), runtime))
