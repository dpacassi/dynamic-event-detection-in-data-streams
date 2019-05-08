from sklearn.metrics import (
    completeness_score,
    homogeneity_score,
    v_measure_score,
    adjusted_rand_score,
    adjusted_mutual_info_score,
    silhouette_score,
)
from sklearn.metrics.cluster import normalized_mutual_info_score
import score


def compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels):
    accuracy, _ = score.cluster_accuracy(true_clusters, predicted_clusters)
    nmi = normalized_mutual_info_score(true_labels, predicted_labels)
    completeness = completeness_score(true_labels, predicted_labels)

    print("------------------")
    print("Example ", nexperiment)
    print("Accuracy: ", accuracy)
    print("NMI: ", completeness)
    print("Completeness: ", completeness)
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


# Thesis Example:
predicted_clusters = [
    [1,2],
    [3,4,5,6],
    [7],
    [8,9]
]

predicted_labels = [1,1,2,2,2,2,3,4,4]

nexperiment += 1
matrix = score.create_accuracy_matrix(true_clusters, predicted_clusters)
print(matrix)
compare_scores(nexperiment, true_clusters, true_labels, predicted_clusters, predicted_labels)
