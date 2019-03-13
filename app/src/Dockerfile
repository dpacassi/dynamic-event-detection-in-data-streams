FROM python:3

WORKDIR /usr/local/src/app

# mariadb client needed for pattern package
RUN sudo apt-get install libmariadbclient-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .