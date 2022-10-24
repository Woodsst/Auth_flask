from pytest import fixture
from sqlalchemy import create_engine
from auth.tests.integration.settings import default_settings
from sqlalchemy.orm import Session
from redis import Redis


@fixture(scope="session")
def postgres_alchemy_con():
    engine = create_engine(default_settings.postgres, convert_unicode=True)
    yield Session(engine)


@fixture(scope="session")
def redis_con():
    con = Redis(
        host=default_settings.redis_host, port=default_settings.redis_port
    )
    yield con
    con.close()
