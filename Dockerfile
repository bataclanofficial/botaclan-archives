FROM python:3.8-slim

ENV PIP_NO_CACHE_DIR=false

RUN apt update -y \
    && apt install -y git \
    && apt install libspotify-dev \
    && rm -rf /var/lib/apt/*

RUN pip install -U poetry

WORKDIR /botaclan

# Install dependencies to optimize layers
COPY pyproject.toml* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Install bot
COPY . .
RUN poetry install --no-dev

ENTRYPOINT ["botaclan"]
