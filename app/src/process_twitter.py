from graph.db import Db
from twitter_api.api import TwitterApi

db = Db()
api = TwitterApi()

topicsWithTweets = api.getTrendsWithTweets(api.SWITZERLAND, limit=2)

for topic, tweets in topicsWithTweets.items():
    db.createEntity('Topic', {'name': topic})

    for tweet in tweets:
        db.createEntity('Tweet', {'created_at': tweet['created_at']})
