from neo4j import GraphDatabase
from .secrets import NEO4J_USERNAME, NEO4J_PASSWORD


class Neo4jDriver:
    uri = "bolt://localhost:7687"

    def __init__(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    def createEntity(self, entity, properties={}):
        with self.driver.session() as session:

            if properties:
                propertyString = self._convertToPropertyString(properties)
                result = session.run(
                    "CREATE (a:{0}{{ {1} }})".format(entity, propertyString))
            else:
                result = session.run(
                    "CREATE (a:{})".format(entity))

            return result

    def createRelationship(self, a, relationship, b):
        raise NotImplementedError()

    def _convertToPropertyString(self, properties):
        return ",".join(['{}:"{}"'.format(key, value) for key, value in properties.items()])
