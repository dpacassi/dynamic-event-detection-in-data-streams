import spacy
import re

from textacy import extract, keyterms, Doc
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

nlp = spacy.load("en_core_web_md")

def remove_html(text):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, " ", text)

    return cleantext


def replace_non_alpha(text):
    text = re.sub("[^a-zA-Z]+", " ", text)

    return text


def replace_page_breaks(text):
    return re.sub(r"(\\n)", r"", text)


def remove_punctuation(text):
    cleaned = re.sub(r"[?|!|\'|#]", r"", text)
    cleaned = re.sub(r"[.|,|)|(|\|/]", r" ", cleaned)

    return cleaned


def remove_multiple_whitespaces(text):
    " ".join(text.split())

    return text


def remove_short_words(text):
    filtered_words = []

    for word in text.split():
        if len(word) > 2:
            filtered_words.append(word)
        else:
            continue

    text = " ".join(filtered_words)

    return text


def f_remove_stopwords(text):
    stop = stopwords.words("english")
    sentences = text.split(".")
    new_text = []

    for sentence in sentences:
        sentence = sentence.strip()

        for word in sentence.split():
            if word not in stop:
                new_text.append(word)

    new_text = " ".join(new_text)

    return new_text


def stem_text(text, remove_stopwords=True):
    stop = stopwords.words("english")
    sno = SnowballStemmer("english")
    sentences = text.split(".")
    stemmed_text = []

    for sentence in sentences:
        sentence = sentence.strip()

        for word in sentence.split():
            if remove_stopwords and word not in stop:
                stemmed_text.append(sno.stem(word))
            elif not remove_stopwords:
                stemmed_text.append(sno.stem(word))

    text = " ".join(stemmed_text)

    return text


def lemmatize_text(text, remove_stopwords=True):
    stop = stopwords.words("english")
    nlp = spacy.load("en", disable=["parser", "ner"])
    sentences = text.split(".")
    lemmatized_text = []

    for sentence in sentences:
        sentence = sentence.strip()
        doc = nlp(sentence)

        if remove_stopwords:
            lemmatized_sentence = " ".join(
                [
                    token.lemma_
                    if token.lemma_ != "-PRON-" and token.lemma_ not in stop
                    else token.lower_
                    for token in doc
                ]
            )
        else:
            lemmatized_sentence = " ".join(
                [
                    token.lemma_ if token.lemma_ != "-PRON-" else token.lower_
                    for token in doc
                ]
            )

        lemmatized_text.append(lemmatized_sentence)

    text = ".".join(lemmatized_text)

    return text


def remove_common_words(text):
    common_words = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
        "year",
        "years",
        "month",
        "months",
        "day",
        "days",
        "hour",
        "hours",
        "minutes",
        "minute",
        "seconds",
        "second",
        "time",
        "date",
        "all",
        "rights",
        "reserved",
        "story",
        "reuters",
        "first",
        "second",
        "third",
        "soon",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "today",
        "now",
    ]
    doc = []

    for word in text.split():
        if word not in common_words:
            doc.append(word)

    text = " ".join(doc)

    return text


def clean_text(text, keep_stopwords=False, use_stemming=False, use_lemmatization=False):
    remove_stopwords = not keep_stopwords

    # Trim text.
    text = text.strip()

    # Transform the text to lower case.
    text = text.lower()

    # Remove page breaks
    text = replace_page_breaks(text)

    # Remove any existing HTML tags.
    text = remove_html(text)

    # Remove common words.
    text = remove_common_words(text)

    # Text lemmatization with spaCy.
    if use_lemmatization:
        text = lemmatize_text(text, remove_stopwords)

    # Text stemming.
    if use_stemming:
        text = stem_text(text, remove_stopwords)

    # Replace all non alphabetical characters with spaces.
    text = replace_non_alpha(text)

    # Remove punctuation.
    # Obsolete since we remove all non alphabetical characters.
    # text = remove_punctuation(text)

    # Remove multiple whitespaces.
    text = remove_multiple_whitespaces(text)

    # Remove short words.
    text = remove_short_words(text)

    return text


def extract_keyterms(data):
    tokens = []
    doc = Doc(data, lang="en_core_web_md")
    res = keyterms.sgrank(doc, n_keyterms=100)

    for r in res:
        tokens.append(str(r[0]))

    if len(tokens) == 0:
        tokens = ["empty"]

    return tokens


def extract_entities(data):
    tokens = []
    doc = Doc(data, lang="en_core_web_md")
    res = extract.named_entities(doc, include_types=["PERSON", "ORG", "LOC"])

    for r in res:
        tokens.append(str(r[0]))

    if len(tokens) == 0:
        tokens = ["empty"]

    return tokens


def extract_keyterms_and_entities(data):
    tokens = extract_keyterms(data)
    tokens += extract_entities(data)

    # Remove duplicates.
    tokens = list(dict.fromkeys(tokens))

    return tokens