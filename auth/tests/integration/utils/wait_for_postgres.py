import logging

import backoff
import psycopg2

logger = logging.getLogger(__name__)


@backoff.on_exception(backoff.expo, psycopg2.OperationalError,
                      max_tries=10, max_time=20,
                      logger=logger.warning(
                          "Пытаемся соединится с постгресом"))
def connect_postgres():
    logger.warning('Повторная попытка соединения с постгрес')
    psycopg2.connect("postgresql://app:123qwe@postgres/clients_database")


if __name__ == "__main__":
    connect_postgres()
