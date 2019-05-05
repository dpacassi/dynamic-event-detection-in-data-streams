# Cluster evaluation

## Tested Methods

affinity_propagation
birch
hdbscan
hdbscan_lda
meanshift
spectral_clustering

## Scores

Normalized mutual information
Completeness score

## Results

### Best score per method

SELECT method, MAX(normalized_mutual_info_score) as nmi,MAX(completeness_score) as completeness FROM `method_evaluation` group by method order by nmi desc

method	nmi   	completeness	
affinity_propagation	0.740863	0.50566	
hdbscan	                0.733162	0.680484	
birch	                0.639539	0.137502	
spectral_clustering	    0.554214	0.43573	
hdbscan_lda	            0.509255	0.425517	
meanshift	            0.33316 	0.058969

#### Context 

SELECT * FROM `method_evaluation` as m WHERE `normalized_mutual_info_score` = (SELECT Max(`normalized_mutual_info_score`) FROM `method_evaluation` m2 where m.method = m2.method) order by normalized_mutual_info_score desc

### Number of estimated clusters vs real

SELECT method, Min(Abs(real_clusters - estimated_clusters)) as difference FROM `method_evaluation` group by method order by difference ASC


method	difference   	
hdbscan	                0	
hdbscan_lda	            1	
affinity_propagation	7	
spectral_clustering	    8	
meanshift	            15	
birch	                451	

#### Context

SELECT * FROM `method_evaluation` as m WHERE Abs(real_clusters - estimated_clusters) = (SELECT Min(Abs(real_clusters - estimated_clusters)) FROM `method_evaluation` m2 where m.method = m2.method)

### Average processing time 

SELECT method, AVG(processing_time) as average_processing_time FROM `method_evaluation` where sample_size = 2000 group by method order by average_processing_time ASC


method	average_processing_time   	
hdbscan	0.29650445949907106	
birch	1.2744041537797008	
affinity_propagation	14.408452648669481	
hdbscan_lda	154.53434733549753	
meanshift	440.7399781545003	
spectral_clustering	461.2059956267476	

## Analyze clusters

### Find news belonging to clusters from a certain evaluation

SELECT n.title, c.id, n.story FROM news_article as n
Join cluster_news_article as cn on cn.news_article_id = n.id
Join cluster as c on c.id = cn.cluster_id
Where c.method_evaluation_id = 1584
order by n.story

### Number of clusters per story (should be 1:1)
SELECT n.story, count(DISTINCT c.id) as nclusters FROM news_article as n
Join cluster_news_article as cn on cn.news_article_id = n.id
Join cluster as c on c.id = cn.cluster_id
Where c.method_evaluation_id = 1584
group by n.story
order by n.story

### Find news articles classified as noise

-- This query can take a couple of minutes.

SELECT * from news_article as nn where nn.story in (
	SELECT n.story FROM news_article as n
	Join cluster_news_article as cn on cn.news_article_id = n.id
	Join cluster as c on c.id = cn.cluster_id
	Where c.method_evaluation_id = 1610 
	group by n.story )
and not exists (
	SELECT c.id FROM cluster_news_article as cna
	Join cluster as c on c.id = cna.cluster_id
	Where c.method_evaluation_id = 1610 and cna.news_article_id = nn.id
)
and newspaper_processed = 1
AND title_keywords_intersection = 1
AND hostname != 'newsledge.com'
AND hostname != 'www.newsledge.com'
AND newspaper_text IS NOT NULL
AND TRIM(COALESCE(newspaper_text, '')) != ''
AND newspaper_text NOT LIKE '%%GDPR%%'
AND newspaper_text NOT LIKE '%%javascript%%'
AND newspaper_text NOT LIKE '%%404%%'
     