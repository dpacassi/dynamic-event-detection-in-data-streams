from graph.db import Db
from newsapi_org.api import NewsApi

from pattern.text import keywords as findKeywords


class ProcessNewsApi:
    def __init__(self):
        self.db = Db()
        self.api = NewsApi()

    def run(self, limit=None):
        headlines = self.api.getHeadlines('ch')
        countryEntity = self.db.createEntity("Country", {"name": "Switzerland"})

        for headline in headlines:
            organisationEntity = self.db.createEntity(
                "Organisation",
                {
                    "name": headline["source"]["name"].lower(),
                },
            )

            newsEntity = self.db.createEntity(
                "News",
                {
                    "author": headline["author"],
                    "title": headline["title"],
                    "description": headline["description"],
                    "url": headline["url"],
                    "urlToImage": headline["urlToImage"],
                    "publishedAt": headline["publishedAt"],
                    "content": headline["content"],
                },
            )

            self.db.createRelationship(newsEntity, "is_relevant_in", countryEntity)
            self.db.createRelationship(newsEntity, "published_by", organisationEntity)

            keywords = findKeywords(headline["title"], language="de")

            for keyword in keywords:
                keywordEntity = self.db.createEntity(
                    "Keyword", {"name": keyword}
                )
                self.db.createRelationship(newsEntity, "mentions", keywordEntity)
