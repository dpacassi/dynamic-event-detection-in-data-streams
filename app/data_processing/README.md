# Data Processing
This module is responsible for preprocessing and clustering of the incoming data stream.

## Setup

The module relies on the scikit-learn development version 0.21.dev which has to be build from source. See the following instructions to install it:  
https://scikit-learn.org/stable/developers/advanced_installation.html#install-bleeding-edge


### Download of additional data
In a shell:
```
python -m spacy download en
```

In a Python shell:
```
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
```
