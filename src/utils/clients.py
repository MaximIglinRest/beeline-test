from typing import Protocol

import psycopg2
from helpers import backoff

from core.config import settings


class PingFailedException(Exception):
    pass


class InvalidClient(Exception):
    pass


class Client(Protocol):
    def check(self):
        pass


class PGClient:
    @backoff()
    def check(self):
        conn = psycopg2.connect(
            user=settings.db_user,
            password=settings.db_password,
            host=settings.postgres_host,
            port=settings.postgres_port,
            database=settings.db_name,
        )
        conn.close()


CLIENTS = {
    "pg": PGClient,
}


def get_client(client: str):
    client_class = CLIENTS.get(client)
    if client_class is None:
        raise InvalidClient
    return client_class()
