import requests
import psycopg2
from pytest import fixture
from redis import Redis

from .settings import default_settings
from .utils.db_requests import clear_table


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

    con = requests.Session()
    yield con
    con.close()


@fixture(scope="function")
def clear_databases(postgres_con, redis_con):
    yield
    clear_table(postgres_con)
    redis_con.execute_command("FLUSHDB")
