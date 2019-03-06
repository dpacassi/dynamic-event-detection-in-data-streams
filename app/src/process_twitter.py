from graph.db import Db
from twitter_api.api import TwitterApi

db = Db()
api = TwitterApi()

topicsWithTweets = api.getTrendsWithTweets(api.SWITZERLAND, limit=2)

for topic, tweets in topicsWithTweets.items():
    topicEntity = db.createEntity('Topic', {'name': topic})

    for tweet in tweets:
        tweetEntity = db.createEntity('Tweet', {'name': tweet['user']['name'], 'created_at': tweet['created_at']})
        db.createRelationship(tweetEntity, "talks_about", topicEntity)
