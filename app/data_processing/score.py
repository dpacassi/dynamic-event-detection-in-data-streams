import collections


def calculate_mp_score(true_clusters, predicted_clusters):
    """
    Calculate the mp_score of a clustering based on the contents of the clusters and the overall difference in
    predicted over true number of clusters. The calculation is based on three steps:
        1. Create an similarity matrix by calculating the difference between each cluster of both clusterings.
        2. Select the most relevant values from the similarity matrix and make sure no two clusters are being used 
           at the same time.
        3. Calculate the average with consideration for differences in number of clusters between true and predicted.
    
    Parameters
    ----------
    true_clusters: array[clusters]
        2-dimensional array of true clusters
    
    predicted_clusters: array[clusters] 
        2-dimensional array of predicted clusters
    """

    # If both clusters are empty, they are identical.
    if len(true_clusters) == 0 and len(predicted_clusters) == 0:
        return 1

    similarity_matrix = create_similarity_matrix(true_clusters, predicted_clusters)
    number_of_true_clusters = len(true_clusters)
    number_of_predicted_clusters = len(predicted_clusters)

    unique_indices = select_max_values(similarity_matrix)

    elements_per_true_cluster = [len(cluster) for cluster in true_clusters]
    elements_per_predicted_cluster = [len(cluster) for cluster in predicted_clusters]
    
    total_true_elements = sum(elements_per_true_cluster)
    total_pred_elements = sum(elements_per_predicted_cluster)
    total_elements = total_true_elements + total_pred_elements

    mp_score = 0
    if total_elements > 0:
        for column, value in unique_indices.items():
            weight =  ((elements_per_true_cluster[value["row_index"]] + elements_per_predicted_cluster[column]) / (total_elements))
            mp_score += value["max_value"] * weight

    return mp_score

def sum_unique_values(unique_indices):
    sum_unique_precision = 0
    for key, value in unique_indices.items():
        sum_unique_precision += value["max_value"]
    return sum_unique_precision

def create_similarity_matrix(true_clusters, predicted_clusters):
    similarity_matrix = []
    for true_cluster in true_clusters:
        true_set = set(true_cluster)
        n_true = float(len(true_set))
        row = []
        for predicted_cluster in predicted_clusters:
            cluster_set = set(predicted_cluster)

            # Calculate the similarity as the jaccard index = |X∩Y| / |X∪Y|
            similarity = len(true_set.intersection(cluster_set)) / len(true_set.union(cluster_set))
            row.append(similarity)

        similarity_matrix.append(row)
    return similarity_matrix

def select_max_values(precision_matrix):
    unique_indices = dict()
    row_index = 0
    nrows = len(precision_matrix)

    while row_index < nrows:
        ignore_indices = set()
        max_value_found = False

        while not max_value_found:
            max_value = 0
            column = 0
            for col_index, value in enumerate(precision_matrix[row_index]):
                if value >= max_value and col_index not in ignore_indices:
                    max_value = value
                    column = col_index

            if (
                max_value > 0
                and column in unique_indices
                and unique_indices[column]["row_index"] != row_index
                and unique_indices[column]["max_value"] > 0
            ):
                if unique_indices[column]["max_value"] < max_value:
                    # The column is already used, but we found a better
                    # candidate. We use the new candidate and set the
                    # cursor to the old one to find a new max value.
                    old_row_index = unique_indices[column]["row_index"]
                    unique_indices[column]["row_index"] = row_index
                    row_index = old_row_index
                    unique_indices[column]["max_value"] = max_value
                    max_value_found = True
                else:
                    # The column is already used by a better candidate.
                    ignore_indices.add(column)
            else:
                # If max_value is greater than 0, we store the value as a
                # new candidate. Otherwise either the row does not match
                # any other column or the max_value was low and got
                # overridden by previous tries and no other match is available.
                if max_value > 0:
                    # The column is free to use
                    unique_indices[column] = {
                        "row_index": row_index,
                        "max_value": max_value,
                    }
                max_value_found = True
                row_index += 1

    return unique_indices