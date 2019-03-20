from azure.cognitiveservices.search.newssearch import NewsSearchAPI
from msrest.authentication import CognitiveServicesCredentials

from .secrets import SUBSCRIPTION_KEY_ENV_NAME


def news_search(subscription_key, query):
    """NewsSearch.
    This will search news for (Quantum  Computing) with market and count parameters then verify number of results and print out totalEstimatedMatches, name, url, description, published time and name of provider of the first news result
    """
    client = NewsSearchAPI(CognitiveServicesCredentials(subscription_key))

    try:
        news_result = client.news.search(query=query, market="de-ch", count=100)
        print("Search news for query \"{}\" with market and count".format(query))

        if news_result.value:
            print("Total estimated matches value: {}".format(news_result.total_estimated_matches))
            print("News result count: {}".format(len(news_result.value)))
            
            for news in news_result.value:
                print("news name: {}".format(news.name))
                print("news url: {}".format(news.url))
                print("news description: {}".format(news.description))
                print("published time: {}".format(news.date_published))
                print("news provider: {}".format(news.provider[0].name))
        else:
            print("Didn't see any news result data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def news_trending(subscription_key):
    """NewsTrending.
    This will search news trending topics in Bing then verify number of results and print out name, text of query, webSearchUrl, newsSearchUrl and image Url of the first news result.
    """
    client = NewsSearchAPI(CognitiveServicesCredentials(subscription_key))

    try:
        trending_topics = client.news.trending(market="de-ch")
        print("Search news trending topics in Bing")

        if trending_topics.value:
            first_topic = trending_topics.value[0]
            print("News result count: {}".format(len(trending_topics.value)))
            print("First topic name: {}".format(first_topic.name))
            print("First topic query: {}".format(first_topic.query.text))
            print("First topic image url: {}".format(first_topic.image.url))
            print("First topic webSearchUrl: {}".format(first_topic.web_search_url))
            print("First topic newsSearchUrl: {}".format(first_topic.news_search_url))
        else:
            print("Didn't see any topics result data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


news_search(SUBSCRIPTION_KEY_ENV_NAME, "Postauto Skandal")
