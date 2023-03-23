FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add build-base
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY src .

COPY entrypoint.sh .
COPY src/utils .

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
