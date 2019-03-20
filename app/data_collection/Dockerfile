FROM python:3.6

WORKDIR /usr/local/src/app

# mariadb client needed for pattern package
RUN apt-get install libmariadbclient-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .