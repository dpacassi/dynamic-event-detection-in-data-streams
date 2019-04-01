import numpy as np
import pandas as pd
import spacy

from hdbscan import HDBSCAN

from gensim.matutils import softcossim
from gensim import corpora
import gensim.downloader as api
from gensim.utils import simple_preprocess

from sklearn.feature_extraction.text import CountVectorizer  # , TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import OPTICS
from sklearn.metrics.pairwise import cosine_similarity

import utils


class ClusterEvaluation:
    def __init__(self, documents, full_dataset=None):
        # Single preprocessing for easy testing of different vectorizers and to reduce redundant computation
        self.data_matrix = CountVectorizer(
            min_df=2, max_df=0.8, lowercase=True, analyzer="word", stop_words="english"
        ).fit_transform(documents)

        self.documents = documents
        self.full_dataset = full_dataset

    ############################

    # HDBSCAN:
    # We use a simple count matrix and cluster it using hdbscan.
    #
    # The reasoning for hdbscan is, that we don't have a fixed number of clusters, since it
    # depends on the given samples. Hdbscan solves this issue by not requiring a fixed number
    # of clusters beforehand as opposed to kmeans. Additionally hdbscan is supposed to solve
    # the issues regarding clusters of varying density of its predecessor dbscan.

    def hdbscan(self):
        labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(
            self.data_matrix
        )
        n_estimated_topics = len(set(labels)) - (1 if -1 in labels else 0)
        return labels, n_estimated_topics

    # Result:
    # Describe it a bit...

    ############################

    # OPTICS:
    # In this second simple approach we use optics instead of hdbscan.
    #
    # Optics is another method which doesn't require a fixed number of clusters and it
    # can work with clusters of varying density.

    def optics(self):
        labels = OPTICS(eps=0.5, min_samples=3).fit_predict(self.data_matrix.todense())
        n_estimated_topics = len(set(labels)) - (1 if -1 in labels else 0)

        return labels, n_estimated_topics

    # Result:
    # The problem with the sklearn implementation of optics is, that it does not work with sparse arrays.
    # Since our word vectors can be quite large, while containing mostly zeros sparse matrices are
    # required for efficient calculations.

    ############################

    # HDBSCAN + LDA:
    # Use hdbscan to estimate number of clusters and use the estimation for the LDA model.
    # Inspired by https://www.multisensorproject.eu/wp-content/uploads/2016/11/2016_GIALAMPOUKIDIS_et_al_MLDM2016_camera_ready_forRG.pdf

    def hdbscan_lda(self):
        hdbscan_labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(
            self.data_matrix
        )
        n_estimated_topics = len(set(hdbscan_labels)) - (
            1 if -1 in hdbscan_labels else 0
        )

        model = LatentDirichletAllocation(n_components=n_estimated_topics).fit(
            self.data_matrix
        )
        document_matrix = model.transform(self.data_matrix)

        lda_labels, documents_by_topic = utils.get_labels_and_documents_from_distribution_matrix(
            document_matrix, self.full_dataset
        )
        return lda_labels, n_estimated_topics

    # Result:
    # Describe it a bit...

    ############################

    # HDBSCAN with entities instead of raw_text:

    def hdbscan_entities(self):
        # The model has to be downloaded first!
        # python -m spacy download en_core_web_sm
        nlp = spacy.load("en_core_web_sm")

        # Extract entities per document with spacy
        # Maybe try different entity extractors? for example MITIE
        def extract_entities(data):
            # https://spacy.io/usage/linguistic-features#named-entities
            doc = nlp(data)
            entities = [entity.text for entity in doc.ents]
            if len(entities) == 0:
                entities = ["empty"]

            return entities

        # Vectorize the entities per document
        data_matrix = CountVectorizer(
            min_df=2,
            max_df=0.95,
            lowercase=True,
            analyzer="word",
            stop_words="english",
            tokenizer=extract_entities,
        ).fit_transform(self.documents)

        labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(data_matrix)
        n_estimated_topics = len(set(labels)) - (1 if -1 in labels else 0)
        return labels, n_estimated_topics

    # Result:
    # Describe it a bit...

    ############################

    # HDBSCAN with cosine similarity:
    # Instead of clustering the data based on the word vector directly, we create a
    # similarity matrix based on the cosine distance between two vectors.
    # This might be the same as using HDBSCAN with metrix cosine though...

    def hdbscan_cossim(self):
        # Create cossim matrix
        cossim_matrix = cosine_similarity(self.data_matrix)

        labels = HDBSCAN(min_cluster_size=3).fit_predict(cossim_matrix)
        n_estimated_topics = len(set(labels)) - (1 if -1 in labels else 0)
        return labels, n_estimated_topics

    ############################

    # HDBSCAN with soft cosine similarity:
    # This approach tries to get better results by using an advanced preprocessing step.
    # It involves entity extraction and calulation the soft cosine similarities of the word matrix.
    # Soft cosine similarities means creating a word vector using a word embedding model, which reduces
    # the distance between similar terms. The cosin_similarity matrix is then used for clustering.
    # Warning: Very slow
    # Ref: https://www.machinelearningplus.com/nlp/cosine-similarity/

    def hdbscan_soft_cossim(self):
        # Download the FastText model
        # python -m gensim.downloader --download fasttext-wiki-news-subwords-300
        fasttext_model300 = api.load("fasttext-wiki-news-subwords-300")

        # Prepare a dictionary and a corpus.
        processed_documents = [simple_preprocess(doc) for doc in self.documents]
        dictionary = corpora.Dictionary(processed_documents)

        # Prepare the similarity matrix
        similarity_matrix = fasttext_model300.similarity_matrix(
            dictionary, tfidf=None, threshold=0.0, exponent=2.0, nonzero_limit=100
        )

        # Create soft cossim matrix
        len_array = np.arange(len(processed_documents))
        xx, yy = np.meshgrid(len_array, len_array)
        cossim_matrix = pd.DataFrame(
            [
                [
                    round(
                        softcossim(
                            processed_documents[i],
                            processed_documents[j],
                            similarity_matrix,
                        ),
                        2,
                    )
                    for i, j in zip(x, y)
                ]
                for y, x in zip(xx, yy)
            ]
        )

        labels = HDBSCAN(min_cluster_size=3).fit_predict(cossim_matrix)
        n_estimated_topics = len(set(labels)) - (1 if -1 in labels else 0)
        return labels, n_estimated_topics

    # Result:
    # Describe it a bit...

    ############################

    def run(self):
        # Run clusterings
        results = []

        labels, n_estimated_topics = self.hdbscan()
        results.append(utils.Result("HDBSCAN", labels, n_estimated_topics))

        labels, n_estimated_topics = self.optics()
        results.append(utils.Result("OPTICS", labels, n_estimated_topics))

        labels, n_estimated_topics = self.hdbscan_lda()
        results.append(utils.Result("HDBSCAN + LDA", labels, n_estimated_topics))

        labels, n_estimated_topics = self.hdbscan_entities()
        results.append(
            utils.Result("HDBSCAN + Entity extraction", labels, n_estimated_topics)
        )

        labels, n_estimated_topics = self.hdbscan_cossim()
        results.append(
            utils.Result(
                "HDBSCAN + Cosine Similarity Matrix", labels, n_estimated_topics
            )
        )

        # Causes a MemoryError and is veeery slow with the current implementation.
        # labels, n_estimated_topics = self.hdbscan_soft_cossim()
        # results.append(
        #     utils.Result(
        #         "HDBSCAN + Soft Cosine Similarity Matrix", labels, n_estimated_topics
        #     )
        # )

        return results


if __name__ == "__main__":
    # Note: Download nlp datasets the first time you run this script.
    # python -m spacy download en_core_web_sm
    # python -m gensim.downloader --download fasttext-wiki-news-subwords-300

    # Load data and setup for evaluation
    content_column = "newspaper_text"
    story_column = "story"

    # Todo: Timing and different sample sets
    dataset = utils.load_test_data(content_column=content_column, nrows=1000)
    labels_true = LabelEncoder().fit_transform(dataset[story_column])

    results = ClusterEvaluation(dataset[content_column], dataset).run()

    print("True number of cluster: %d" % len(set(labels_true)))

    # Print resultsdataset
    for result in results:
        result.print_evaluation(labels_true)
