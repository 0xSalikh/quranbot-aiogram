FROM python:3.9.9-slim-buster AS development_build
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && pip install poetry

WORKDIR /code

COPY pyproject.toml poetry.lock /code/
RUN poetry install --no-dev
COPY src .
