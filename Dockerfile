FROM python:3.8 as django
COPY . /app/
WORKDIR /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM node:20.7 as npm
WORKDIR /app/




