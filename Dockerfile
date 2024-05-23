FROM python:3.8 as django
COPY . /app/
WORKDIR /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DB_NAME postgres
ENV DB_USER postgres
ENV DB_PASSWORD postgres
ENV DB_HOST pgdb
ENV DB_PORT 5432
ENV CHANNELS_HOST redis
ENV CHANNELS_PORT 6379
ENV REDIS_HOST redis://redis:6379

FROM node:20.7 as npm
WORKDIR /app/
COPY package-lock.json /app/
COPY package.json /app/

FROM nginx:1.24 as nginx
COPY ./config-nginx.d/default.conf /etc/nginx/conf.d/default.conf
WORKDIR /var/www/html/



