import pandas
import utils


filepath = "test_data/clean_news.csv"

test_data = pandas.read_csv(filepath, nrows=None)

noise = []
errors = 0

for index, row in test_data.iterrows():
    try:
        keywords_content = set(row['newspaper_keywords'].split(','))

        keywords_title = row['title'].lower()
        keywords_title = utils.remove_punctuation(keywords_title)
        keywords_title = set(keywords_title.split())

        # If there are no intersections, we can assume this article to be faulty.
        if not keywords_content.intersection(keywords_title):
            # print("{}; {}; {}".format(row['id'], row['title'], row['newspaper_text'],))
            noise.append(index)
    except AttributeError:
        # If there is an error while accessing the data, it is most likely broken.
        noise.append(index)
        errors += 1

test_data.drop(noise)
test_data.to_csv("test_data/clean_news_less_noisy.csv", index=False, header=False)


print()
print(len(noise))
print(errors)
