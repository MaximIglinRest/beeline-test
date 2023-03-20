FROM python:3.10-alpine
WORKDIR /tests
COPY . .
COPY settings utils/settings
COPY settings src/settings
CMD python -m pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir --ignore-installed\
    && python utils/wait_for_es.py \
    && python utils/wait_for_redis.py \
    && pytest src
