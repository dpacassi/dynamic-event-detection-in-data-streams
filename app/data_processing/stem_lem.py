import re
import time
import spacy

from textacy import extract, keyterms, Doc
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

nlp = spacy.load("en_core_web_md")
stop = stopwords.words("english")
sno = SnowballStemmer("english")


def lemmatize_word(a_word):
    doc = nlp(a_word)

    for token in doc:
        return token.lemma_


def stem_word(a_word):
    return sno.stem(a_word)


words = ['written', 'greatest', 'best', 'fastest', 'highest', 'compute', 'computer', 'computed', 'computing', 'studies', 'studying', 'university', 'universities', 'universe', 'universal']
stemmed = []
lemmatised = []

start_time = time.time()
for word in words:
    w = lemmatize_word(word)
    lemmatised.append(w)
    # print(word + ' -> ' + w)
end_time = time.time()
total_time = (end_time - start_time) * 1000
print("Lemmatization took %f ms" % (total_time))

start_time = time.time()
for word in words:
    w = stem_word(word)
    stemmed.append(w)
    # print(word + ' -> ' + w)
end_time = time.time()
total_time = (end_time - start_time) * 1000
print("Stemming took %f ms" % (total_time))

print("")

for idx, word in enumerate(words):
    print(words[idx] + " & " + stemmed[idx] + " & " + lemmatised[idx] + " \\\\ \\hline")
