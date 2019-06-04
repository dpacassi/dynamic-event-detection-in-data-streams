# Data processing proposal
- trends/place
  - Retrieve all 5 minutes
  - The API always returns 50 trends
  - The trends don't change very rapidly
- search/tweets
  - Retrieve for all trends every 5 minutes
  - The API returns up to 100 tweets
    - The tweets are from around the last 2 hours (if German tweets are processed)
  - Make use of [since_id](https://developer.twitter.com/en/docs/tweets/timelines/guides/working-with-timelines)
  - This is where **trend shift detection** can be done!
- newsapi.org
  - Retrieve top headlines and everything for Switzerland, every 10 minutes
  - This is where **trend shift detection** can be done!

## Keyword/keyphrase extraction
- API's only provide between 1'000 and 10'000 free requests per month
- We need to evaluate custom solutions
- Do we have enough machine power for this though?

### Proposed API
Amazon Comprehend. Check [features](https://aws.amazon.com/comprehend/features/) and [pricing](https://aws.amazon.com/comprehend/pricing/).

### Proposed custom solutions
- [NLP/N-Grams/TF IDF](https://medium.com/analytics-vidhya/automated-keyword-extraction-from-articles-using-nlp-bfd864f41b34)
- [github.com/boudinfl/pke](https://github.com/boudinfl/pke)
- [github.com/csurfer/rake-nltk](https://github.com/csurfer/rake-nltk)
- [github.com/aneesha/RAKE](https://github.com/aneesha/RAKE)
- [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/)
