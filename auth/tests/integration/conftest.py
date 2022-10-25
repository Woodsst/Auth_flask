import http.client

import psycopg2
from pytest import fixture
from redis import Redis

from auth.tests.integration.settings import default_settings


@fixture(scope="session")
def postgres_con():
    """Соединение с постгресом"""

    con = psycopg2.connect(default_settings.postgres)
    yield con
    con.close()


@fixture(scope="session")
def redis_con():
    """Соединение с Редисом"""

    con = Redis(
        host=default_settings.redis_host, port=default_settings.redis_port
    )
    yield con
    con.close()


@fixture(scope="session")
def http_con():
    """http клиент"""

    con = http.client.HTTPConnection(
        host=default_settings.host_app, port=default_settings.port_app
    )
    yield con
    con.close()
