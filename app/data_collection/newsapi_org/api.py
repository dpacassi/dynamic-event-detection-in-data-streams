from newsapi import NewsApiClient
from .secrets import (
    NEWSAPIORG_API_KEY,
)


class NewsApi:

    def __init__(self):
        self.api = NewsApiClient(api_key=NEWSAPIORG_API_KEY)

    def getHeadlines(self, country):
        headlines = self.api.get_top_headlines(country=country, page_size=100)

        return headlines['articles']
