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
            if headline["source"]["name"]:
                organisationEntity = self.db.createEntity(
                    "Organisation",
                    {
                        "name": headline["source"]["name"].lower(),
                    },
                )

            newsObject = {}

            if headline["author"]:
                newsObject["author"] = headline["author"]

            if headline["title"]:
                newsObject["title"] = headline["title"]

            if headline["description"]:
                newsObject["description"] = headline["description"]

            if headline["url"]:
                newsObject["url"] = headline["url"]

            if headline["urlToImage"]:
                newsObject["urlToImage"] = headline["urlToImage"]

            if headline["publishedAt"]:
                newsObject["publishedAt"] = headline["publishedAt"]

            if headline["content"]:
                newsObject["content"] = headline["content"]

            newsEntity = self.db.createEntity(
                "News",
                newsObject,
            )

            self.db.createRelationship(newsEntity, "is_relevant_in", countryEntity)
            self.db.createRelationship(newsEntity, "published_by", organisationEntity)

            keywords = findKeywords(headline["title"], language="de")

            for keyword in keywords:
                keywordEntity = self.db.createEntity(
                    "Keyword", {"name": keyword}
                )
                self.db.createRelationship(newsEntity, "mentions", keywordEntity)
