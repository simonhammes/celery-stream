FROM python:3.11-slim AS builder

ENV POETRY_CACHE_DIR=/opt/.cache
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app

RUN pip install "poetry==1.8.4"

COPY pyproject.toml poetry.lock /app/

RUN --mount=type=cache,target=${POETRY_CACHE_DIR} poetry install --no-root

FROM python:3.11-slim

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app.py tasks.py /app/
COPY templates/ /app/templates/

EXPOSE 5000

CMD ["python", "app.py"]
