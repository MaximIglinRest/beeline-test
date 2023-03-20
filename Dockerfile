FROM python:3.10-alpine

WORKDIR /app

COPY src .
COPY requirements.txt .

RUN apk add build-base
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

CMD gunicorn main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker
