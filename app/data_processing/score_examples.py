from sklearn.metrics import (
    completeness_score,
    homogeneity_score,
    v_measure_score,
    adjusted_rand_score,
    adjusted_mutual_info_score,
    silhouette_score,
    normalized_mutual_info_score,
    fowlkes_mallows_score
)
import score
import pprint

from clusim.clustering import Clustering
import clusim.sim as sim


def compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels):
    avg_similarity, weighted_similarity = score.cluster_similarity(true_clusters, predicted_clusters)
    nmi = normalized_mutual_info_score(true_labels, predicted_labels, average_method='arithmetic')
    completeness = completeness_score(true_labels, predicted_labels)
    v_measure = v_measure_score(true_labels, predicted_labels)
    rand = adjusted_rand_score(true_labels, predicted_labels)
    fms = fowlkes_mallows_score(true_labels, predicted_labels)

    T = Clustering()
    C = Clustering()
    T.from_cluster_list(true_clusters)
    C.from_cluster_list(predicted_clusters)

    jaccard_index = sim.jaccard_index(T, C)
    nmi2 = sim.nmi(T, C)
    fmeasure = sim.fmeasure(T, C)
    element_sim = sim.element_sim(T, C)

    print("------------------")
    print("Example ", nexperiment)
    print("AVG Similarity: ", round(avg_similarity,3))
    print("Weigthed Similarity: ", round(weighted_similarity,3))
    print("NMI: ", round(nmi,3))
    print("NMI2: ", round(nmi2,3))
    print("Completeness: ", round(completeness,3))
    print("V-Measure: ", round(v_measure,3))
    print("Adjusted Rand: ", round(rand,3))
    print("Fowlkes Mallows: ", round(fms,3))
    print("Jaccard Index: ", round(jaccard_index,3))
    print("F-Measure: ", round(fmeasure,3))
    print("Element-centric: ", round(element_sim,3))
    print()


# Example 1: Ideal clusterings
true_clusters = [
    [1,2,3],
    [4,5,6,7],
    [8,9]
]

predicted_clusters = [
    [1,2,3],
    [4,5,6,7],
    [8,9]
]

# NMI and completeness need one dimensional labeled arrays.
true_labels = [1,1,1,2,2,2,2,3,3]
predicted_labels = [1,1,1,2,2,2,2,3,3]

nexperiment = 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)


# Example 2: Nonideal clusterings
predicted_clusters = [
    [1,2],
    [3,4,5,6],
    [7,8,9]
]

predicted_labels = [1,1,2,2,2,2,3,3,3]

nexperiment += 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)

# Example 3: ntrue < npredicted
predicted_clusters = [
    [1,2,3],
    [4,5,6],
    [7],
    [8,9]
]

predicted_labels = [1,1,1,2,2,2,3,4,4]

nexperiment += 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)

# Example 4: ntrue < npredicted
predicted_clusters = [
    [1,2,3],
    [4,5],
    [6,7],
    [8],
    [9]
]

predicted_labels = [1,1,1,2,2,3,3,4,5]

nexperiment += 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)

# Example 5: ntrue < npredicted
predicted_clusters = [
    [1],
    [2],
    [3],
    [4],
    [5],
    [6],
    [7],
    [8],
    [9]
]

predicted_labels = [1,2,3,4,5,6,7,8,9]

nexperiment += 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)


# Example 6: ntrue > npredicted
predicted_clusters = [
    [1,2,3,4,5],
    [6,7,8,9],
]

predicted_labels = [1,1,1,1,1,2,2,2,2]

nexperiment += 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)

# Example 7: ntrue > npredicted
predicted_clusters = [
    [1,2,3,4,5,6,7,8,9],
]

predicted_labels = [1,1,1,1,1,1,1,1,1]

nexperiment += 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)


# Example 8: same shape/number of clusters but different content
predicted_clusters = [
    [7,2,4],
    [8,9,6,3],
    [1,5]
]

predicted_labels = [3,1,2,1,3,2,1,2,2]
nexperiment += 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)
matrix = score.create_similarity_matrix(true_clusters, predicted_clusters)
pprint.pprint(matrix)
print()

# Example 9

predicted_clusters = [
    [1,2,3,4,5,6,7,8], [9],
]

predicted_labels = [1,1,1,1,1,1,1,1,2]

nexperiment += 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)


# Thesis example:
predicted_clusters = [
    [1,2],
    [3,4,5,6],
    [7],
    [8,9]
]

predicted_labels = [1,1,2,2,2,2,3,4,4]

compare_scores('Thesis example', true_clusters, true_labels, predicted_clusters, predicted_labels)
matrix = score.create_similarity_matrix(true_clusters, predicted_clusters)
pprint.pprint(matrix)
print()

# Example 10: Pacassis example 1
true_clusters = [
    list(range(1, 1001)),
    [2000],
    [3000]
]
true_labels = 1000 * [1]
true_labels += [2, 3]

predicted_clusters = [
    list(range(1, 1001)),
    [2000,3000]
]
predicted_labels = 1000 * [1]
predicted_labels += [2, 2]

nexperiment += 1
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)
matrix = score.create_similarity_matrix(true_clusters, predicted_clusters)
pprint.pprint(matrix)
print()

# Similarity:  0.5
# NMI:  0.954
# NMI2:  0.954
# Completeness:  1.0
# V-Measure:  0.954
# Adjusted Rand:  1.0
# Fowlkes Mallows:  1.0
# Jaccard Index:  1.0
# F-Measure:  1.0
# Element-centric:  0.999


# # Example 10: Pacassis example 2
# true_clusters = [
#     list(range(1, 1001)),
#     [2000],
#     [3000]
# ]
# true_labels = 1000 * [1]
# true_labels += [2, 3]

# predicted_clusters = [
#     list(range(1, 1001)),
#     [4000],
#     [5000]
# ]
# predicted_labels = list(range(1, 1001))
# predicted_labels += [4000, 5000]

# nexperiment += 1
# compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)
# matrix = score.create_similarity_matrix(true_clusters, predicted_clusters)
# pprint.pprint(matrix)
# print()