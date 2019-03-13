import twitter
from .secrets import (
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
)


class TwitterApi:

    GLOBAL = 1
    SWITZERLAND = 23424957
    API_MAX_COUNT = 100

    def __init__(self):
        self.api = twitter.Api(
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET,
            access_token_key=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
            sleep_on_rate_limit=True
        )

    def getTrendsWithTweets(self, countryId, languages, limit=None):
        trendingTopics = self.api.GetTrendsWoeid(countryId)

        if limit:
            trendingTopics = trendingTopics[:limit]

        for topic in trendingTopics:
            tweets = []
            for lang in languages:
                tweets.extend(self.api.GetSearch(term=topic.name, lang=lang, count=100))
            yield topic, [t.AsDict() for t in tweets]