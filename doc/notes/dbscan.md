<!--
https://medium.com/@elutins/dbscan-what-is-it-when-to-use-it-how-to-use-it-8bd506293818
-->

# K-means clustering
k-means clustering is an iterative clustering method which assigns all data points in a given data set
into k clusters, where k is a predefined number of clusters in the dataset.

## How does k-means clustering work
At the very beginning, k-means creates k centroids at random locations.
It then repeats following instructions until reaching convergence:

- For each data point: Find the nearest centroid
- Assign the data point to the nearest centroid (cluster)
- For each cluster: Compute a new cluster centroid with all assigned data points

## Advantages
- Very simple and easy to understand algorithm

## Disadvantages
- Initial (random) centroids have a strong impact on the results
- The number of clusters (k) has to be known beforehand
- Unable to handle noise (all data points will be assigned to a cluster)

# DBSCAN
DBSCAN stands for *Density-Based Spatial Clustering of Applications with Noise*
and is a density based clustering algorithm.

A big advantage of DBSCAN is that it's able to sort data into clusters
of different shapes.

## How does DBSCAN work
DBSCAN requires two parameters in order to work:
1. epsilon - The maximum distance between two data points for them to be considered as in the same cluster.
2. minPoints - The number of data points a neighborhood has to contain in order to be considered as a cluster.

Having these two parameters defined, DBSCAN will iterate through the data points
and try to assign them to clusters if the provided parameters match.
If a data point can't be assigned to a cluster, it will be marked as noise point.

Data points that belong to a cluster but don't dense themselves are known
as **border points**. Some border points could theoretically belong to two or more clusters
if the distance from the point to the clusters don't differ. 

## Advantages
- Does not need to know the number of clusters beforehand
- Is able to find shaped clusters
- Is able to handle noise points

## Disadvantages
- DBSCAN is not entirely deterministic
- Defining the right epsilon value can be difficult
- Unable to cluster data sets with large differences in densities

# HDBSCAN
