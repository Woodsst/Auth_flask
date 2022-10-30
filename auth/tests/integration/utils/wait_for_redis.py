import logging

import backoff
import redis

logger = logging.getLogger(__name__)


@backoff.on_exception(
    backoff.expo,
    redis.exceptions.ConnectionError,
    max_tries=10,
    max_time=20,
    logger=logger.warning("Пытаемся соединится с редисом"),
)
def connect_postgres():
    r = redis.Redis(host="redis", port=6379)
    logger.warning("Повторная попытка соединения с редис")
    r.ping()


if __name__ == "__main__":
    connect_postgres()
