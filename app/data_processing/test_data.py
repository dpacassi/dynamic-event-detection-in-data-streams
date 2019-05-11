import db
import pandas


def load_from_csv(nrows=1000, skip_rows=0):
    filepath = "test_data/clean_news_less_noisy.csv"

    names = [
        "id",
        "title",
        "url",
        "publisher",
        "category",
        "story",
        "hostname",
        "date",
        "newspaper_processed",
        "newspaper_meta_language",
        "newspaper_keywords",
        "newspaper_text",
    ]
    test_data = pandas.read_csv(
        filepath, nrows=nrows, skiprows=skip_rows, header=None, names=names
    )

    return test_data[test_data["newspaper_text"].notnull()]


def load_from_db(nrows=1000, skip_rows=0):
    connection = db.get_connection()

    get_sql = (
        "SELECT id, newspaper_text, story"
        " FROM news_article"
        " WHERE"
        "     newspaper_processed = 1"
        "     AND title_keywords_intersection = 1"
        "     AND hostname != 'newsledge.com'"
        "     AND hostname != 'www.newsledge.com'"
        "     AND newspaper_text IS NOT NULL"
        "     AND TRIM(COALESCE(newspaper_text, '')) != ''"
        "     AND newspaper_text NOT LIKE '%%GDPR%%'"
        "     AND newspaper_text NOT LIKE '%%javascript%%'"
        "     AND newspaper_text NOT LIKE '%%404%%'"
        "     AND newspaper_text NOT LIKE '%%cookie%%'"
        " ORDER BY id ASC"
        " LIMIT %s, %s"
    )

    data = pandas.read_sql(
        sql=get_sql, con=connection, index_col="id", params=[skip_rows, nrows]
    )
    connection.close()

    return data


def load_from_db_by_stories(nstories, skip_stories=0):
    connection = db.get_connection()

    story_sql = (
        "SELECT story"
        " FROM news_article"
        " WHERE newspaper_processed = 1"
        "     AND title_keywords_intersection = 1"
        "     AND hostname != 'newsledge.com'"
        "     AND hostname != 'www.newsledge.com'"
        "     AND newspaper_text IS NOT NULL"
        "     AND TRIM(COALESCE(newspaper_text, '')) != ''"
        "     AND newspaper_text NOT LIKE '%%GDPR%%'"
        "     AND newspaper_text NOT LIKE '%%javascript%%'"
        "     AND newspaper_text NOT LIKE '%%404%%'"
        "     AND newspaper_text NOT LIKE '%%cookie%%'"
        "     AND preprocessed = 1"
        " GROUP BY story"
        " LIMIT %s, %s"
    )

    stories = pandas.read_sql(
        sql=story_sql, con=connection, params=[skip_stories, nstories]
    )

    story_ids = ",".join(["'" + x + "'" for x in stories["story"]])

    news_sql = (
        "SELECT id, newspaper_text, story, text_keyterms, text_entities, text_keyterms_and_entities, text_lemmatized_without_stopwords, text_stemmed_without_stopwords"
        " FROM news_article"
        " WHERE"
        "     newspaper_processed = 1"
        "     AND story in ({})"
        "     AND title_keywords_intersection = 1"
        "     AND hostname != 'newsledge.com'"
        "     AND hostname != 'www.newsledge.com'"
        "     AND newspaper_text IS NOT NULL"
        "     AND TRIM(COALESCE(newspaper_text, '')) != ''"
        "     AND newspaper_text NOT LIKE '%%GDPR%%'"
        "     AND newspaper_text NOT LIKE '%%javascript%%'"
        "     AND newspaper_text NOT LIKE '%%404%%'"
        "     AND newspaper_text NOT LIKE '%%cookie%%'"
        "     AND preprocessed = 1"
        " ORDER BY id ASC".format(story_ids)
    )

    data = pandas.read_sql(sql=news_sql, con=connection, index_col="id")
    connection.close()
    return data
