# Data clustering

## Goal

To detect events of a certain significance and to find common denominators, we use clustering to find news articles belonging to the same story.

## Evaluation

https://en.wikipedia.org/wiki/Silhouette_(clustering)
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html

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
* Sensitive to varying densities

#### Relevant Papers

* http://homepages.vub.ac.be/~ndeligia/pubs/TwitterDataClusteringVisual.pdf
* https://www.multisensorproject.eu/wp-content/uploads/2016/11/2016_GIALAMPOUKIDIS_et_al_MLDM2016_camera_ready_forRG.pdf


### HDBSCAN

**Pros**
* Improvement of dbscan and less sensitive for varying densities

### Optics

### Affinity Propagation

#### Relevant Papers 
* http://www.cnergres.iitkgp.ac.in/subeventsummarizer/dataset.html

### Birch

### LDA
* http://www.aclweb.org/anthology/D13-1068