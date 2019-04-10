import numpy as np
import pandas as pd
import spacy
import collections
import argparse
import time

from textacy import extract, keyterms, Doc
from dotenv import load_dotenv

from pattern.text import keywords as findKeywords
from scipy.sparse import find

from hdbscan import HDBSCAN
from datasketch import MinHash, MinHashLSH

from gensim.matutils import softcossim
from gensim import corpora
import gensim.downloader as api
from gensim.utils import simple_preprocess

from sklearn.feature_extraction.text import CountVectorizer , TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import Birch  # , OPTICS
from sklearn.metrics.pairwise import cosine_similarity

import utils


class ClusterEvaluation:
    def __init__(self, documents, full_dataset=None):
        # Single preprocessing for easy testing of different vectorizers and to reduce redundant computation
        vectorizer = CountVectorizer(
            min_df=3, max_df=0.9, lowercase=True, analyzer="word", stop_words="english"
        ).fit(documents)

        self.data_matrix = vectorizer.transform(documents)
        features = vectorizer.get_feature_names()

        # Extract entities from sparse data_matrix
        self.features_by_document = utils.map_features_to_word_vectors(self.data_matrix, features)

        self.documents = documents
        self.full_dataset = full_dataset

        self.excluded_entity_types = ['CARDINAL', 'ORDINAL', 'QUANTITY']

    ############################

    # HDBSCAN:
    # We use a simple count matrix and cluster it using hdbscan.
    #
    # The reasoning for hdbscan is, that we don't have a fixed number of clusters, since it
    # depends on the given samples. Hdbscan solves this issue by not requiring a fixed number
    # of clusters beforehand as opposed to kmeans. Additionally hdbscan is supposed to solve
    # the issues regarding clusters of varying density of its predecessor dbscan.

    def hdbscan(self):
        start = time.time()
        labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(
            self.data_matrix
        )
        end = time.time()
        return labels, (end - start)

    # Result:
    # First 1000 news articles with 27 clusters:
    # Estimated number of clusters: 46
    # Completeness: 0.644
    # NMI score: 0.627

    ############################

    # OPTICS:
    # In this second simple approach we use optics instead of hdbscan.
    #
    # Optics is another method which doesn't require a fixed number of clusters and it
    # can work with clusters of varying density.

    def optics(self):
        start = time.time()
        labels = OPTICS(eps=0.5, min_samples=3).fit_predict(self.data_matrix.todense())
        end = time.time()

        return labels, (end - start)

    # Result:
    # The problem with the sklearn implementation of optics is, that it does not work with sparse arrays.
    # Since our word vectors can be quite large, while containing mostly zeros, sparse matrices are
    # required for efficient calculations. Additionally it can be observed that the score is much lower
    # than hdbscan. This is why we use hdbscan for the following clustering tasks.
    #
    # First 1000 news articles with 27 clusters:
    # Number of clusters: 21
    # Completeness: 0.304
    # NMI score: 0.100

    ############################

    # Birch:
    # TODO: explain why birch
    # Ref: https://www.researchgate.net/profile/Basavaraju_Mallikarjunappa/publication/45601907_A_Novel_Method_of_Spam_Mail_Detection_using_Text_Based_Clustering_Approach/links/54cb016a0cf2517b7560cc9d/A-Novel-Method-of-Spam-Mail-Detection-using-Text-Based-Clustering-Approach.pdf

    def birch(x):
        # https://scikit-learn.org/stable/modules/clustering.html#birch
        start = time.time()
        labels = Birch(
            branching_factor=50, n_clusters=None, threshold=0.25, compute_labels=True
        ).fit_predict(x)
        end = time.time()

        return labels, (end - start)

    # Result:
    # First 1000 news articles with 27 clusters:

    ############################

    ############################

    # BIRCH with entities instead of raw_text:

    def birch_entities(self):
        # The model has to be downloaded first!
        # python -m spacy download en_core_web_sm
        start = time.time()
        nlp = spacy.load("en_core_web_sm")

        # Extract entities per document with spacy
        # Maybe try different entity extractors? for example MITIE
        def extract_entities(data):
            # https://spacy.io/usage/linguistic-features#named-entities
            doc = nlp(data)
            entities = []
            for entity in doc.ents:
                if entity.label_ not in self.excluded_entity_types:
                    entities.append(entity.text)

            if len(entities) == 0:
                entities = ["empty"]

            return entities

        # Vectorize the entities per document
        data_matrix = CountVectorizer(
            min_df=1,
            max_df=3,
            lowercase=True,
            analyzer="word",
            stop_words="english",
            tokenizer=extract_entities,
        ).fit_transform(self.documents)

        labels = Birch(
            branching_factor=50, n_clusters=None, threshold=0.25, compute_labels=True
        ).fit_predict(data_matrix)
        end = time.time()

        return labels, (end - start)

    # Result:

    ############################

    # HDBSCAN + LDA:
    # Use hdbscan to estimate number of clusters and use the estimation for the LDA model.
    # Inspired by https://www.multisensorproject.eu/wp-content/uploads/2016/11/2016_GIALAMPOUKIDIS_et_al_MLDM2016_camera_ready_forRG.pdf

    def hdbscan_lda(self):
        start = time.time()
        hdbscan_labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(
            self.data_matrix
        )

        n_estimated_topics = len(set(hdbscan_labels)) - (1 if -1 in hdbscan_labels else 0)
        model = LatentDirichletAllocation(n_components=n_estimated_topics, max_iter=50).fit(
            self.data_matrix
        )
        document_matrix = model.transform(self.data_matrix)

        lda_labels, documents_by_topic = utils.get_labels_and_documents_from_distribution_matrix(
            document_matrix, self.full_dataset
        )
        end = time.time()

        return lda_labels, (end - start)

    # Result:
    # First 1000 news articles with 27 clusters:
    # Number of clusters: 46
    # Completeness: 0.563
    # NMI score: 0.619

    ############################

    # HDBSCAN with entities instead of raw_text:

    def hdbscan_entities(self):
        start = time.time()

        # The model has to be downloaded first!
        # python -m spacy download en_core_web_sm
        nlp = spacy.load("en_core_web_md")

        # Extract entities per document with spacy
        # Maybe try different entity extractors? for example MITIE
        def extract_entities(data):
            # https://spacy.io/usage/linguistic-features#named-entities
            doc = nlp(data)
            entities = []
            for entity in doc.ents:
                if entity.label_ not in self.excluded_entity_types:
                    entities.append(entity.text)

            if len(entities) == 0:
                entities = ["empty"]

            return entities

        # Vectorize the entities per document
        vectorizer = CountVectorizer(
            min_df=1,
            max_df=0.8,
            # analyzer="word",
            # stop_words="english",
            tokenizer=extract_entities,
        ).fit(self.documents)

        data_matrix = vectorizer.transform(self.documents)
        features = vectorizer.get_feature_names()

        # Extract entities from sparse data_matrix
        features_by_document = utils.map_features_to_word_vectors(data_matrix, features)

        labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(data_matrix)
        end = time.time()

        return labels, features_by_document, (end - start)

    # Result:
    # First 1000 news articles with 27 clusters:
    # Number of clusters: 63
    # Completeness: 0.339
    # NMI score: 0.311

    # Result David:
    # First 1000 news articles with 27 clusters:
    # Number of clusters: 60
    # Completeness: 0.302
    # NMI score: 0.287

    # Result David (after applying text preprocessing and adapting min_df and max_df):
    # First 1000 news articles with 27 clusters:
    # Number of clusters: 23
    # Completeness: 0.755
    # NMI score: 0.70
    
    ############################

    # HDBSCAN with tokens instead of raw_text:

    def hdbscan_keywords(self):
        start = time.time()

        def extract_keywords(data):
            entities = findKeywords(data, language='en')
            if len(entities) == 0:
                entities = ["empty"]

            return entities

        # Vectorize the entities per document
        vectorizer = CountVectorizer(
            min_df=1,
            max_df=0.8,
            # analyzer="word",
            # stop_words="english",
            tokenizer=extract_keywords,
        ).fit(self.documents)

        data_matrix = vectorizer.transform(self.documents)
        features = vectorizer.get_feature_names()

        # Extract entities from sparse data_matrix
        features_by_document = utils.map_features_to_word_vectors(data_matrix, features)

        labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(data_matrix)
        end = time.time()

        return labels, features_by_document, (end - start)

    # Result:
    # First 1000 news articles with 27 clusters:
    # Number of clusters: 0
    # Completeness: 0.0
    # NMI score: 0.0

    ############################

    # HDBSCAN with keyterms and entities instead of raw_text:

    def hdbscan_keyterms_and_entities(self):
        start = time.time()

        def extract_keyterms_and_entities(data):
            tokens = []
            doc = Doc(data, lang='en_core_web_md')
            res = extract.named_entities(doc, include_types=['PERSON', 'ORG', 'LOC'])
            for r in res:
                tokens.append(str(r[0]))

            res = keyterms.sgrank(doc, n_keyterms=50)
            for r in res:
                tokens.append(str(r[0]))

            if len(tokens) == 0:
                tokens = ["empty"]

            return tokens

        # Vectorize the entities per document
        vectorizer = TfidfVectorizer(
            min_df=2,
            max_df=0.8,
            # analyzer="word",
            # stop_words="english",
            tokenizer=extract_keyterms_and_entities,
        ).fit(self.documents)

        data_matrix = vectorizer.transform(self.documents)
        features = vectorizer.get_feature_names()

        # Extract entities from sparse data_matrix
        features_by_document = utils.map_features_to_word_vectors(data_matrix, features)

        labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(data_matrix)
        n_estimated_topics = len(set(labels)) - (1 if -1 in labels else 0)
        end = time.time()

        return labels, n_estimated_topics, features_by_document, (end - start)

    # Result:
    # First 1000 news articles with 27 clusters:
    # Number of clusters: 0
    # Completeness: 0.0
    # NMI score: 0.0

    ############################

    # HDBSCAN with cosine similarity:
    # Instead of clustering the data based on the word vector directly, we create a
    # similarity matrix based on the cosine distance between two vectors.
    # This might be the same as using HDBSCAN with metrix cosine though...

    def hdbscan_cossim(self):
        # Create cossim matrix
        start = time.time()
        cossim_matrix = cosine_similarity(self.data_matrix)

        labels = HDBSCAN(min_cluster_size=3).fit_predict(cossim_matrix)
        end = time.time()

        return labels, (end - start)

    # Result:
    # First 1000 news articles with 27 clusters:
    # Number of clusters: 79
    # Completeness: 0.577
    # NMI score: 0.632

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
        start = time.time()
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
        end = time.time()

        return labels, (end - start)

    # Result:
    # So far not runnable due to memory restrictions.

    ############################

    # Keyterms + MinHash + LSH
    # Ref: https://ekzhu.github.io/datasketch/lsh.html
    def minhash_lsh(self):
        start = time.time()
        hashes = []

        # Create LSH index
        lsh = MinHashLSH(threshold=0.99, num_perm=128)

        for index, document in enumerate(self.documents):
            hash = MinHash(num_perm=128)
            entities = findKeywords(document, language='en')

            for entity in entities:
                hash.update(str.encode(entity, 'utf-8'))
            
            hashes.append(hash)
            lsh.insert(index, hash)

        # TODO: Check if n_estimated_topics is correctly build in utils.py
        n_estimated_topics = 0
        processed_indices = []
        for index, hash in enumerate(hashes):
            matches = lsh.query(hash)
            if len(matches) > 1 and index not in processed_indices:
                n_estimated_topics += 1
                processed_indices += matches

        # print("Approximate neighbours with Jaccard similarity > 0.5", result)
        end = time.time()

        return range(len(hashes)), (end - start)
    
    # Result:
    # Todo: describe result.

    ############################

    def run(self, methods):
        # Run clusterings
        results = []

        if 'hdbscan' in methods:
            labels, processing_time = self.hdbscan()
            results.append(utils.Result("HDBSCAN", labels, processing_time))

        if 'optics' in methods:
            labels, processing_time = self.optics()
            results.append(utils.Result("OPTICS", labels, processing_time))

        if 'birch' in methods:
            labels, processing_time = self.birch()
            results.append(utils.Result("BIRCH", labels, processing_time))

        if 'birch_entities' in methods:
            labels, processing_time = self.birch_entities()
            results.append(utils.Result("Birch + Entity extraction", labels, processing_time))

        if 'hdbscan_lda' in methods:
            labels, processing_time = self.hdbscan_lda()
            results.append(utils.Result("HDBSCAN + LDA", labels, processing_time))

        if 'hdbscan_entities' in methods:
            labels, features, processing_time = self.hdbscan_entities()
            results.append(
                utils.Result("HDBSCAN + Entity extraction", labels, processing_time, features)
            )

        if 'hdbscan_keywords' in methods:
            labels, features, processing_time = self.hdbscan_keywords()
            results.append(
                utils.Result("HDBSCAN + Keyword extraction", labels, processing_time, features)
            )

        if 'hdbscan_keyterms_and_entities' in methods:
            labels, n_estimated_topics, features, processing_time = self.hdbscan_keyterms_and_entities()
            results.append(
                utils.Result("HDBSCAN + Keyterm + Entity extraction", labels, n_estimated_topics, processing_time, features)
            )

        if 'hdbscan_cossim' in methods:
            labels, processing_time = self.hdbscan_cossim()
            results.append(
                utils.Result(
                    "HDBSCAN + Cosine Similarity Matrix", labels, processing_time
                )
            )

        if 'hdbscan_soft_cossim' in methods:
            # Causes a MemoryError and is veeery slow with the current implementation.
            labels, processing_time = self.hdbscan_soft_cossim()
            results.append(
                utils.Result(
                    "HDBSCAN + Soft Cosine Similarity Matrix", labels, processing_time
                )
            )

        if 'minhash_lsh' in methods:
            labels, processing_time = self.minhash_lsh()
            results.append(utils.Result("MinHash + LSH", labels, processing_time))

        return results


if __name__ == "__main__":
    # Note: Download nlp datasets the first time you run this script.
    # python -m spacy download en_core_web_md
    # python -m gensim.downloader --download fasttext-wiki-news-subwords-300

    # Load environment variables.
    load_dotenv()

    # Handle arguments.
    ap = argparse.ArgumentParser()
    ap.add_argument('--methods', required=False, type=str, default="hdbscan_entities")
    ap.add_argument('--rows', required=False, type=int, default=1000)
    ap.add_argument('--skip-rows', required=False, type=int, default=0)
    ap.add_argument('--source', required=False, type=str, default='database')
    ap.add_argument('--show-details', dest='show_details', action='store_true')
    ap.set_defaults(show_details=False)
    ap.add_argument('--keep-stopwords', dest='keep_stopwords', action='store_true')
    ap.set_defaults(keep_stopwords=False)
    ap.add_argument('--use-stemming', dest='use_stemming', action='store_true')
    ap.set_defaults(use_stemming=False)
    ap.add_argument('--use-lemmatization', dest='use_lemmatization', action='store_true')
    ap.set_defaults(use_lemmatization=False)
    args = vars(ap.parse_args())

    # Load data and setup for evaluation
    id_column = "id"
    content_column = "newspaper_text"
    headline_column = "title"
    story_column = "story"

    if args['source'] == 'csv':
        dataset = utils.load_test_data(nrows=args['rows'], skip_rows=args['skip_rows'], keep_stopwords=args['keep_stopwords'], use_stemming=args['use_stemming'], use_lemmatization=args['use_lemmatization'])
    else:
        dataset = utils.load_test_data_from_db(nrows=args['rows'], skip_rows=args['skip_rows'], keep_stopwords=args['keep_stopwords'], use_stemming=args['use_stemming'], use_lemmatization=args['use_lemmatization'])

    labels_true = LabelEncoder().fit_transform(dataset[story_column])
    results = ClusterEvaluation(dataset[content_column], dataset).run(args['methods'].split(','))

    print("True number of clusters: %d" % len(set(labels_true)))
    print("")

    # Print resultsdataset
    for result in results:
        result.print_evaluation(labels_true)

        if args['show_details'] and result.features is not None:
            print(len(result.features))
            grouped_indices = collections.defaultdict(list)
            for index, value in enumerate(result.labels):
                if value >= 0:
                    grouped_indices[value].append(index)

            for key, indices in grouped_indices.items():
                print("Group %d: \n" % key)
                # print(indices)
                for index in indices:
                    print("{}: {}".format(dataset[id_column][index], dataset[headline_column][index]))
                    # print("Entities: {}".format(result.features[index] if index < len(result.features) else "no entities"))
                print("------------------------------")

            print(result.labels)
            print(result.n_topics)
