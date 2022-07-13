FROM python:3.8.10-slim-buster

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install ffmpeg libsm6 libxext6  -y

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY pyproject.toml /app/

RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

RUN pwd

RUN ls -ltr
