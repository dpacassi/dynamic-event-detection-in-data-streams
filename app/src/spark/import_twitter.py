import sys
import requests
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SQLContext

conf = SparkConf()
conf.setAppName("Trending Twitter")

sparkContext = SparkContext(conf=conf)
sparkContext.setLogLevel("ERROR")

intervalSize = 2
streamingContext = StreamingContext(sparkContext, intervalSize)
streamingContext.checkpoint("checkpoint_twitter_import")

dataStream = streamingContext.socketTextStream("localhost", 9009)

