from graph.db import Db
from twitter_api.api import TwitterApi


class ProcessTwitter:
    def __init__(self):
        self.db = Db()
        self.api = TwitterApi()

    def run(self, limit=None):
        topicsWithTweets = self.api.getTrendsWithTweets(self.api.SWITZERLAND, limit)
        for topic, tweets in topicsWithTweets:
            topicEntity = self.db.createEntity("Topic", {"name": topic.name})
            # topicEntity = db.createEntity('Topic', {'name': topic.name, 'created_at': topic.timestamp})

            for tweet in tweets:
                tweetEntity = self.db.createEntity(
                    "Tweet",
                    {"name": tweet["user"]["name"], "created_at": tweet["created_at"]},
                )
                self.db.createRelationship(tweetEntity, "talks_about", topicEntity)


# Execute directly for development/debugging reasons.
if __name__ == "__main__":
    processor = ProcessTwitter()
    processor.run(limit=2)
