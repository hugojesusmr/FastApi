FROM python:3.12-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache gcc musl-dev mysql-dev python3-dev libffi-dev \
    && pip install --upgrade pip

COPY requirements.txt /code/requirements.txt

RUN pip install -r  /code/requirements.txt

COPY . /code/
WORKDIR /code/

CMD ["sh", "entrypoint.sh"]

