import twitter
from secrets import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                  consumer_secret=TWITTER_CONSUMER_SECRET,
                  access_token_key=TWITTER_ACCESS_TOKEN,
                  access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
