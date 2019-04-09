from .neo4j_driver import Neo4jDriver


class GraphDb:

    def __init__(self):
        self.driver = Neo4jDriver()

    def createEntity(self, entity, properties={}):
        return self.driver.createEntity(entity, properties)

    def createRelationship(self, a, relationship, b):
        return self.driver.createRelationship(a, relationship, b)
