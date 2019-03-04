from api import api

chWoeid = 23424957
trendingTopics = api.GetTrendsWoeid(chWoeid)

trendingTopicsWithTweets = {}
for topic in trendingTopics:
    tweets = api.GetSearch(term=topic.name)
    trendingTopicsWithTweets[topic.name] = [t.AsDict() for t in tweets]

    # break for testing reasons
    break

print(trendingTopicsWithTweets)
