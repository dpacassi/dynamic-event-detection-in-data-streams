import spacy
import time
import argparse
import json
import math
import numpy as np

from itertools import chain
from textacy import extract, keyterms, Doc
from dotenv import load_dotenv
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import Birch, AffinityPropagation, MeanShift, SpectralClustering, KMeans

import utils


nlp = spacy.load("en_core_web_md")


# Cluster methods inside a class (pun intended) since some methods rely on a global state e.g. documents
class ClusterMethods:
    def __init__(self, documents, preprocessed_documents):
        self.documents = documents
        self.preprocessed_documents = preprocessed_documents

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
        hdbscan_labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(data_matrix)

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
        n_approx = int(math.sqrt(len(self.documents)))
        start = time.time()

        km = KMeans(
            n_clusters=n_approx
        ).fit(data_matrix)
        labels = km.predict(data_matrix)

        end = time.time()
        return labels, (end - start)

    def setup_evaluation(self):
        def extract_entities(data):
            # https://spacy.io/usage/linguistic-features#named-entities
            doc = nlp(data)
            entities = []
            for entity in doc.ents:
                if entity.label_ not in ["CARDINAL", "ORDINAL", "QUANTITY"]:
                    entities.append(entity.text)

            if len(entities) == 0:
                entities = ["empty"]

            return entities

        def extract_keyterms_and_entities(data):
            tokens = []
            doc = Doc(data, lang="en_core_web_md")
            res = extract.named_entities(doc, include_types=["PERSON", "ORG", "LOC"])
            for r in res:
                tokens.append(str(r[0]))

            res = keyterms.sgrank(doc, n_keyterms=100)
            for r in res:
                tokens.append(str(r[0]))

            if len(tokens) == 0:
                tokens = ["empty"]

            return tokens

        vectorizers = [
            CountVectorizer(
                min_df=3,
                max_df=0.9,
                lowercase=True,
                analyzer="word",
                stop_words="english",
                max_features=100000,
                dtype=np.int32
            ),
            TfidfVectorizer(
                min_df=3,
                max_df=0.9,
                lowercase=True,
                analyzer="word",
                stop_words="english",
                max_features=100000,
                dtype=np.int32
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
            #self.kmeans: {
            #    "n_range": [5]
            #},
            self.hdbscan: {
                "min_cluster_size": [5, 6],  # range(3, 7),
                "metric": ["cosine", "euclidean", "manhattan"]
                # "metric": ["cosine", "minkowski", "euclidean"]
            },
            # self.meanshift: {"cluster_all": [True, False]},
            # self.birch: {
            #     "branching_factor": range(10, 100, 10),
            #     # "threshold": range(2, 6),
            # },
            # self.affinity_propagation: {
            #     "affinity": ["euclidean"],
            #     "convergence_iter": [15],
            #     "damping": np.arange(0.5, 0.9, 0.1),
            #     "max_iter": [50, 100, 200, 500],
            # },
            # self.spectral_clustering: {
            #     "affinity": ["rbf"],
            #     "assign_labels": ["kmeans", "discretize"],
            # },
            # self.hdbscan_lda: {"max_iter": [50, 100, 200, 500]},
            # minhash_lsh: {'threshold': range(0.1, 0.9, 0.1), 'min_cluster_size': range(2, 6)},
        }

        return vectorizers, tokenizers, parameters_by_method

    def run(self):
        vectorizers, tokenizers, parameters_by_method = self.setup_evaluation()
        results = []
        errors = []

        for vectorizer in vectorizers:
            for tokenizer in tokenizers:
                print(
                    "Use vectorizer {} with tokenizer {}".format(
                        vectorizer.__class__.__name__,
                        "None" if tokenizer is None else tokenizer.__name__,
                    )
                )

                if tokenizer is None:
                    data_matrix = vectorizer.fit_transform(self.preprocessed_documents)
                else:
                    vectorizer.set_params(tokenizer=tokenizer)
                    data_matrix = vectorizer.fit_transform(self.documents)

                print(len(vectorizer.get_feature_names()))
                exit()

                for method, parameters in parameters_by_method.items():
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
                        #try:
                        labels, processing_time = method(
                            data_matrix, **parameter_combination
                        )

                        results.append(
                            utils.Result(
                                method.__name__,
                                labels,
                                processing_time,
                                None,
                                vectorizer.__class__.__name__,
                                "None" if tokenizer is None else tokenizer.__name__,
                                parameter_combination,
                            )
                        )
                        # except BaseException as error:
                        #     errors.append(
                        #         "Error while running {}: Message {}; Vectorizer {}; Tokenizer {}; Parameters {}; ".format(
                        #             method.__name__,
                        #             error,
                        #             vectorizer.__class__.__name__,
                        #             "None" if tokenizer is None else tokenizer.__name__,
                        #             str(parameter_combination),
                        #         )
                        #     )
        return results, errors

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
    ap.add_argument("--runs", required=False, type=int, default=1)
    args = vars(ap.parse_args())

    number_of_runs = args["runs"]
    nrows = args["rows"]

    load_dotenv()

    start = time.time()

    for run in range(number_of_runs):
        print("Start run {}".format(run))
        preprocessed_dataset = utils.load_test_data(
            nrows=nrows,
            skip_rows=run * nrows,
            keep_stopwords=False,
            use_stemming=False,
            use_lemmatization=False,
        )
        full_dataset = preprocessed_dataset  # utils.load_test_data(
        #     nrows=nrows,
        #     skip_rows=run * nrows,
        #     keep_stopwords=True,
        #     use_stemming=False,
        #     use_lemmatization=False,
        # )

        evaluation = ClusterMethods(
            full_dataset["newspaper_text"], preprocessed_dataset["newspaper_text"]
        )
        labels_true = LabelEncoder().fit_transform(full_dataset["story"])
        results, errors = evaluation.run()

        for result in results:
            scores = result.create_evaluation(labels_true)
            utils.write_evaluation_result_in_db(
                str(result.title),
                int(nrows),
                str(result.vectorizer),
                str(result.tokenizer),
                str(json.dumps(result.parameters)),
                float(scores["normalized_mutual_info_score"]),
                float(scores["completeness_score"]),
                float(scores["adjusted_mutual_info_score"]),
                int(scores["n_clusters"]),
                int(len(set(labels_true)) - (1 if -1 in labels_true else 0)),
                int(scores["n_noise"]),
                float(result.processing_time),
            )

        if len(errors) > 0:
            print("Errors:")
            print(errors)
        print("Finished run {} with {} errors.".format(run, len(errors)))

    end = time.time()
    runtime = end - start
    print("Finished Evaluation after {}s.".format(len(errors), runtime))
