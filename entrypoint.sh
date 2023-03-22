#!/bin/sh
python wait_for_pg.py
alembic upgrade head
gunicorn main:app --bind 0.0.0.0:8000 \
-k uvicorn.workers.UvicornWorker