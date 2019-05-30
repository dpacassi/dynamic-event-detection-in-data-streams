import spacy
from textacy import extract, keyterms, Doc

# sentence = 'London is the capital and most populous city of England and the United Kingdom.'
# sentence = 'Mr. Best flew to New York on Saturday morning.'
sentence = 'Trump says he will increase tariffs on Chinese goods on Friday as he complains about pace of trade talks.'

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

print("Keyterms:")
res = keyterms.sgrank(doc, n_keyterms=100)
for r in res:
    print(r)
