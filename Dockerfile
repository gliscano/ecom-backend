
# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /code
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh /code/

# copy project
COPY . /code/

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]