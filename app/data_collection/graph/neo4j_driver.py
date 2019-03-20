import os

from neo4j import GraphDatabase
from .secrets import NEO4J_USERNAME, NEO4J_PASSWORD
from .entity import Entity


class Neo4jDriver:

    def __init__(self):
        self.uri = os.getenv('NEO4J_URI', "bolt://localhost:7687")
        self.driver = GraphDatabase.driver(self.uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    def createEntity(self, entityName, properties={}):
        with self.driver.session() as session:

            if properties:
                # We use string concatenation instead of parameters because MERGE does not work with parameters.
                # The reason for using MERGE instead of CREATE is the prevention of duplicates.
                # This solution is bad practice and will be refactored later on.
                propertyString = self._convertToPropertyString(properties)
                result = session.run(
                    "MERGE (a:{}{{ {} }}) RETURN a".format(entityName, propertyString))
            else:
                result = session.run(
                    "CREATE (a:{}) RETURN a".format(entityName))

            record = result.single()[0]
            return Entity(entityName=entityName, id=record.id)  # , properties=record.properties)

    def createRelationship(self, firstEntity, relationship, secondEntity):
        with self.driver.session() as session:
            result = session.run(
                    "MATCH (a:{}),(b:{}) "
                    "WHERE id(a) = {} AND id(b) = {} "
                    "MERGE (a)-[r:{}]->(b) "
                    "RETURN r"
                    .format(firstEntity.name, secondEntity.name, firstEntity.id, secondEntity.id, relationship))

            return result

    def _convertToPropertyString(self, properties):
        return ",".join(['{}:"{}"'.format(key, self._escapeCharacters(value)) for key, value in properties.items()])

    def _escapeCharacters(self, rawString):
        escapeChars = ['\\', '"']
        return ''.join(['\\' + c if c in escapeChars else c for c in rawString])
