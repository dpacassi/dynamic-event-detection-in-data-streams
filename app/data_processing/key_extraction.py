import spacy
from textacy import extract, keyterms, Doc

# sentence = 'London is the capital and most populous city of England and the United Kingdom.'
# sentence = 'Mr. Best flew to New York on Saturday morning.'
# sentence = 'Trump says he will increase tariffs on Chinese goods on Friday as he complains about pace of trade talks.'
sentence = 'CERN in Geneva pays tribute to Murray Gell-Mann, who won the Nobel Prize in Physics in 1969.'

'''
# Run first following command in a shell:
# > python -m spacy download en_core_web_lg
doc = Doc(sentence, lang='en_core_web_lg')
res = extract.named_entities(doc)

for r in res:
    print(r)
# This only prints following entities: London, England, United Kingdom
'''

nlp = spacy.load('en_core_web_md')
doc = nlp(sentence)

print("Entities:")
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
print("")

print("Keyterms (sgrank):")
res = keyterms.sgrank(doc, n_keyterms=100)
for r in res:
    print(r)
print("")

'''
print("Keyterms (textrank):")
res = keyterms.textrank(doc, n_keyterms=100)
for r in res:
    print(r)
print("")

print("Keyterms (singlerank):")
res = keyterms.singlerank(doc, n_keyterms=100)
for r in res:
    print(r)
print("")

print("Keyterms (semantic network):")
res = keyterms.key_terms_from_semantic_network(doc, n_keyterms=100)
for r in res:
    print(r)
print("")
'''
