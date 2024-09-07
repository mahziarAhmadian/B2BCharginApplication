# Dockerfile for Locust service

FROM locustio/locust:latest

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app