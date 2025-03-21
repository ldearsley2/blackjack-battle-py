FROM python:3.13-slim

RUN pip install --upgrade pip \
    && pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root

COPY . /app

EXPOSE 5000

CMD ["poetry", "run", "main"]