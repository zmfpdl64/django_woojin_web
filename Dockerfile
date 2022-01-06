#pull offical base image
FROM python:3.8.0-alpine

#set work directory
WORKDIR /usr/src/app

# set enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev libffi-dev

COPY . /usr/src/app/

#install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
