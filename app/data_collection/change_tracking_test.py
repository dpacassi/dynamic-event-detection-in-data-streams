import collections

from graph.graph_db import GraphDb

from pattern.text import keywords as findKeywords

import textacy

db = GraphDb()


def update_graph(topic, keywords):
    additions_per_topic = collections.defaultdict(list)

    for keyword in keywords:
        entity, creation_result = db.createEntity("Keyword", {"name": keyword})
        relationship_result = db.createRelationship(entity, "belongs_to", topic)

        # if creation_result.summary() is not None and creation_result.summary().counters.nodes_created > 0:
        #    print("New Node: {}".format(keyword))

        if relationship_result.summary() is not None and relationship_result.summary().counters.relationships_created > 0:
            # print("New Relationship: {}".format(keyword))
            additions_per_topic[topic.properties['name']].append(keyword)
            # Maybe add all parents of the new keyword entity? 
        
    return additions_per_topic


text = '''
     The shuttle Discovery, already delayed three times by technical problems 
     and bad weather, was grounded again Friday, this time by a potentially 
     dangerous gaseous hydrogen leak in a vent line attached to the shipʼs 
     external tank. The Discovery was initially scheduled to make its 39th 
     and final flight last Monday, bearing fresh supplies and an intelligent 
     robot for the International Space Station. But complications delayed the 
     flight from Monday to Friday,  when the hydrogen leak led NASA to conclude 
     that the shuttle would not be ready to launch before its flight window 
     closed this Monday.
 '''


# CFLAGS="-Wno-narrowing" pip install cld2-cffi
keywords = findKeywords(text, language='en')

topic_one, _ = db.createEntity("Topic", {"name": "Mother"})
topic_two, _ = db.createEntity("Topic", {"name": "Bla"})

print(update_graph(topic_one, keywords))
print(update_graph(topic_one, keywords))
print(update_graph(topic_one, ["test"]))
print(update_graph(topic_two, ["test"]))
