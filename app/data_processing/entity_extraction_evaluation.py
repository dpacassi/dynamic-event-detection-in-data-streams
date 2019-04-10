import spacy
import textacy
from textacy import keyterms

from nltk.parse import CoreNLPParser
# from nltk import word_tokenize, pos_tag, ne_chunk

import utils
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

# python -m spacy download en_core_web_md
# python -m spacy download en_core_web_lg

text = 'paris/london/atlanta: federal reserve bank of philadelphia president charles plosser, who votes on policy this year, said recent encouraging economic data isn’t enough to change the pace of the central bank’s asset purchases.\n\n“it would have been nice, from my perspective, had we started at a faster pace," plosser said in a bloomberg television interview with manus cranny in paris, referring to the fed’s tapering of its stimulus programme. “given the fact that we’ve embarked on measured reductions, it’s important to give some certainty or at least clarity to the markets on what we’re doing. it’s ok to continue at $10 billion. the hurdle rate for change is pretty high in either direction."\n\nthe fed is trying to determine whether the economy has shown recent signs of weakness because of severe winter weather or fundamental obstacles to growth. the policy-setting federal open market committee (fomc) meets 18-19 march in its first gathering led by chair janet yellen since she succeeded ben s. bernanke last month.\n\nnew york fed president william c. dudley said on 7 march he sees a “reasonably favorable" outlook for the economy, even as high unemployment and low inflation warrant stimulus for a “considerable time."\n\nthe us employers added more workers than projected in february, data last week showed, indicating the economy is starting to bounce back from a weather-induced setback. the 175,000 gain in employment followed a revised 129,000 increase the prior month that was bigger than initially estimated.\n\nno whip-saw\n\nimprovement in the labour market is one reason the fomc has trimmed monthly bond purchases by $10 billion in each of its past two meetings. the central bank in january reduced monthly bond purchases to $65 billion.\n\npolicy shouldn’t be “whip-sawed from month to month," plosser said when asked about the jobs numbers. the numbers were “encouraging," though they follow other data in the previous two months that were “weak," he said.\n\nyellen has pledged to press on with gradual reductions in so-called quantitative easing so long as the economy continues to show signs of improvement.\n\nthe fed has pledged to keep the main interest rate at zero well past the time unemployment falls below 6.5%. labour department figures showed that joblessness rose to 6.7% in february from 6.6% the month before as more people entered the labour force and couldn’t find work.\n\nplosser, a former university of rochester economist, became president of the philadelphia fed in august 2006. the bank’s district includes eastern pennsylvania, southern new jersey and delaware. bloomberg\n\njennifer ryan in london contributed to this story.'
text = utils.replace_page_breaks(text)

# nlp = spacy.load("en_core_web_sm")

# doc = nlp(text)
# print("spacy sm:")
# for entity in doc.ents:
#     print("{} ({})".format(entity.text, entity.label_))


# print("---------------")
# nlp = spacy.load("en_core_web_md")

# doc = nlp(text)
# print("spacy md:")
# for entity in doc.ents:
#     print("{} ({})".format(entity.text, entity.label_))

# print("---------------")
# nlp = spacy.load("en_core_web_lg")

# doc = nlp(text)
# print("spacy lg:")
# for entity in doc.ents:
#     print("{} ({})".format(entity.text, entity.label_))

# print("---------------")
# print("nltk with corenlp:")

# corenlp = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
# tokens = corenlp.tokenize(text)
# ner = corenlp.tag(tokens)

# print(tokens)
# print(ner)

# https://github.com/Lynten/stanford-corenlpfrom stanfordcorenlp import StanfordCoreNLP
# CoreNLP Server has to be running: docker-compose up corenlp
# from stanfordcorenlp import StanfordCoreNLP
# nlp = StanfordCoreNLP('http://localhost', port=9000)
# print(nlp.ner(text))

# nlp.close()


# notes:
# use a higher weight for certain entities
# extract noun phrases and individual nouns, verbs etc. combine them as tokens.

# CFLAGS="-Wno-narrowing" pip install cld2-cffi
text = textacy.preprocess.normalize_whitespace(text)
doc = textacy.Doc(text, lang='en_core_web_md')

print(text)

print("---------------")
print("noun_chunks:")

res = textacy.extract.noun_chunks(doc)
for r in res:
    print(r)

print("---------------")
print("named_entities:")

res = textacy.extract.named_entities(doc)
for r in res:
    print(r)

print("---------------")
print("sgrank:")

res = keyterms.sgrank(doc, n_keyterms=50)
for r in res:
    print(r)

print("---------------")
print("singlerank:")

res = keyterms.singlerank(doc, n_keyterms=50)
for r in res:
    print(r)

print("---------------")
print("textrank:")

res = keyterms.textrank(doc, n_keyterms=50)
for r in res:
    print(r)


print("---------------")
print("key_terms_from_semantic_network:")

res = keyterms.key_terms_from_semantic_network(doc, n_keyterms=50)
for r in res:
    print(r)

