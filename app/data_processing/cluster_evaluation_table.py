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

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import Birch, OPTICS
from sklearn.metrics.pairwise import cosine_similarity

import utils


def hdbscan(data_matrix, **parameters):
    start = time.time()
    labels = HDBSCAN(**parameters).fit_predict(data_matrix)
    end = time.time()
    return labels, (end - start)


def optics(data_matrix, **parameters):
    start = time.time()
    labels = OPTICS(**parameters).fit_predict(data_matrix.todense())
    end = time.time()
    return labels, (end - start)


def birch(data_matrix, **parameters):
    # https://scikit-learn.org/stable/modules/clustering.html#birch
    #         branching_factor=50, n_clusters=None, threshold=0.25, compute_labels=True
    start = time.time()
    labels = Birch(n_clusters=None, **parameters).fit_predict(data_matrix)
    end = time.time()
    return labels, (end - start)


def hdbscan_lda(data_matrix, **parameters):
    start = time.time()
    hdbscan_labels = HDBSCAN(min_cluster_size=3, metric="cosine").fit_predict(data_matrix)

    n_estimated_topics = len(set(hdbscan_labels)) - (1 if -1 in hdbscan_labels else 0)
    model = LatentDirichletAllocation(n_components=n_estimated_topics, **parameters).fit(
        data_matrix
    )
    document_matrix = model.transform(data_matrix)

    lda_labels, documents_by_topic = utils.get_labels_and_documents_from_distribution_matrix(
        document_matrix, self.full_dataset
    )
    end = time.time()

    return lda_labels, (end - start)


# TODO make ready for experiment
# Keyterms + MinHash + LSH
# Ref: https://ekzhu.github.io/datasketch/lsh.html
def minhash_lsh(data_matrix, **parameters):
    start = time.time()
    hashes = []

    # Create LSH index
    lsh = MinHashLSH(num_perm=128, **parameters)

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
    
    
def extract_entities(data):
    # https://spacy.io/usage/linguistic-features#named-entities
    doc = nlp(data)
    entities = []
    for entity in doc.ents:
        if entity.label_ not in ['CARDINAL', 'ORDINAL', 'QUANTITY']:
            entities.append(entity.text)

    if len(entities) == 0:
        entities = ["empty"]

    return entities


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


# Setup experiment

vectorizers = [
    CountVectorizer(
            min_df=3, max_df=0.9, lowercase=True, analyzer="word", stop_words="english"
        ),
    TfidfVectorizer(
            min_df=3, max_df=0.9, lowercase=True, analyzer="word", stop_words="english"
        )
]

tokenizers = [
    None,
    extract_entities,
    extract_keyterms_and_entities,
    # TODO word2vec
]

parameters_by_method = {
    hdbscan: {'min_cluster_size': range(2, 6)},
    optics: {'eps': np.arange(0.1, 0.9, 0.1), 'min_cluster_size': range(2, 6)},
    birch: {'branching_factor': range(10, 100, 10), 'min_cluster_size': range(2, 6)},
    hdbscan_lda: {'max_iter': range(10, 100, 10)},
    # minhash_lsh: {'threshold': range(0.1, 0.9, 0.1), 'min_cluster_size': range(2, 6)},
}

documents = ''
preprocessed_documents = ''
results = []


def extract_parameters(keys, values, param_chain, i):
    key = keys[i]
    parameter_combinations = []
    for value in values[i]:
        param_chain[key] = value
        new_chain = extract_parameters(keys, values, param_chain, i + 1) if i < len(keys) - 1 else param_chain
        parameter_combinations.append(new_chain.copy())

    return parameter_combinations


for vectorizer in vectorizers:
    for tokenizer in tokenizers:

        if tokenizers is None:
            vectorizer.fit_transform(preprocessed_documents)
        else:
            vectorizer.set_params(tokenizer=tokenizer)
            vectorizer.fit_transform(documents)

        for method, parameters in parameters_by_method.items():
            keys = list(parameters.keys())
            values = list(parameters.values())
            parameter_combinations = extract_parameters(keys, values, {}, 0)

            for parameter_combination in parameter_combinations:
                labels, runtime = method(parameter_combination)


