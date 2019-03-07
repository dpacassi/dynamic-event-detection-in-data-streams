from graph.db import Db
from twitter_api.api import TwitterApi


class ProcessTwitter:
    def __init__(self):
        self.db = Db()
        self.api = TwitterApi()

    def run(self, limit=None):
        topicsWithTweets = self.api.getTrendsWithTweets(
            self.api.SWITZERLAND, ["en", "de"], limit
        )
        countryEntity = self.db.createEntity("Country", {"name": "Switzerland"})

        for topic, tweets in topicsWithTweets:
            topicEntity = self.db.createEntity("Topic", {"name": topic.name})
            self.db.createRelationship(topicEntity, "is_relevant_in", countryEntity)
            for tweet in tweets:
                tweetEntity = self.db.createEntity(
                    "Tweet",
                    {
                        "text": tweet["text"],
                        "created_at": tweet["created_at"],
                        "lang": tweet["lang"],
                    },
                )

                if "name" in tweet["user"]:
                    userEntity = self.db.createEntity(
                        "User", {"name": tweet["user"]["name"]}
                    )
                    self.db.createRelationship(tweetEntity, "belongs_to", userEntity)

                self.db.createRelationship(tweetEntity, "talks_about", topicEntity)
