# Dynamic Event Detection in Data Streams

## Abstract
Detecting events in data streams can be difficult,
especially if the definition, content, or properties of an event change over time.

This bachelor thesis focuses on the development and evaluation of an online clustering solution
in which events are defined either as changes in existing clusters or as the formation of new clusters.
The solution is a text mining software, which receives new news articles over a data stream and processes them.
Articles are assigned to different clusters due to their similarity to other articles.
The assumption is that very similar articles write about the same news story.
In addition, the evaluation of the clustering quality is measured with a custom scoring function.

The first part of this work consists of determining a suitable data set,
which will be the subject of the clustering and provides the ground truth for evaluating the results.
The implemented solution uses HDBSCAN as the clustering method
and compares it with the state-of-the-art method *k*-means.
It turned out that the use of HDBSCAN has advantages over *k*-means in terms of both performance and precision.
Furthermore, various text preprocessing methods and vector space models are evaluated,
with Text Lemmatization and tf-idf providing the most promising results.
Once applied in a simulated online setting,
the final evaluation found that the noise rate in the overall clustering reduces the precision in the event detection.

The resulting precision of the clustering is 72% with a standard deviation of 12%.
The precision for detecting new events results in 62% with a standard deviation of 43%.
Detecting changes in existing events results in a precision 69% with a standard deviation of 16%.
A continuation of this work should focus on improving the overall clustering to increase the precision of the event detection.

## Thesis
See [doc/thesis.pdf](doc/thesis.pdf).

## Authors
- [Daniel Milenkovic](http://danielmilenkovic.me/)
- [David Pacassi Torrico](https://pacassi.ch/)

## Supervisors
- [Dr. Andreas Weiler](https://www.zhaw.ch/de/ueber-uns/person/wele/)
- [Prof. Dr. Kurt Stockinger](https://www.zhaw.ch/de/ueber-uns/person/stog/)

