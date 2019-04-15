FROM python:3.6

WORKDIR /usr/local/src/data_processing

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_md
RUN python -m spacy download en
RUN python -m nltk.downloader all

COPY . .
