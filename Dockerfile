FROM python:3.8-slim

ENV PIP_NO_CACHE_DIR=false

RUN pip install -U poetry

WORKDIR /botaclan

COPY pyproject.toml* ./

RUN poetry config virtualenvs.create false \
    && poetry install

COPY . .

ENTRYPOINT [ "python" ]
CMD ["-m", "botaclan"]
