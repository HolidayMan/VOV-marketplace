ARG IMAGE_VERSION=python:3.11.2-alpine
ARG PLATFORM=linux/amd64

###########
# BUILDER #
###########

# pull official base image
FROM --platform=${PLATFORM} ${IMAGE_VERSION} as builder

# create the appropriate directories
ENV APP_HOME=/app/web
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements.txt
ADD ./requirements.txt .

# install psycopg2 dependencies
RUN set -ex \
    && apk update \
    && apk add --no-cache --virtual .build-deps postgresql-dev gcc python3-dev \
    musl-dev zlib-dev jpeg-dev build-base libwebp-dev linux-headers curl-dev\
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install awscli

# copy project
COPY . .
ADD media .
ADD static .

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["./entrypoint.sh"]
