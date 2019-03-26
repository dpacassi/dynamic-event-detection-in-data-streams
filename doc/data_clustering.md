# Data clustering

## Goal

To detect events of a certain significance and to find common denominators, we use clustering to find news articles belonging to the same story.

## Evaluation


## Problems

tfidf works fine offline but not online. Maybe consider HashingVectorizer or CountVectorizer.

## TODos
* cite papers
* find working approach
* use sklearn pipelines
* look into stemming for preprocessing
* consensus clustering with a consensus matrix

## Approaches

Find papers referencing useful clustering methodologies for our use case.

### DBSCAN

**Pros**

* Works with noise, which means not all data points have to belong to a cluster
* Doesn't require predefined number of clusters
* Doesn't assume spherical cluster formation

**Cons**

* So far not very accurate (but the training data is very rough...)


#### Relevant Papers

http://homepages.vub.ac.be/~ndeligia/pubs/TwitterDataClusteringVisual.pdf

### Optics

### Affinity Propagation

### Birch

