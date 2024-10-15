FROM python:3.11-slim

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY app.py tasks.py /app/
COPY templates/ /app/templates/

EXPOSE 5000

CMD ["python", "app.py"]
