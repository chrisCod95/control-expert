# base image
FROM python:3.6-slim

COPY . /app

WORKDIR /app

RUN apt-get update

RUN apt-get install -y software-properties-common

RUN apt-get update

RUN apt-get install -y nginx git 

RUN apt install -y php

RUN apt-get install -y php-curl

RUN pip install -r requirements.txt

COPY nginx.conf /etc/nginx/sites-enabled/default

ENV ENV_FILE_LOCATION ./.env

RUN chmod +x ./start.sh

CMD ["./start.sh"]

ENV ENV_FILE_LOCATION ./.env