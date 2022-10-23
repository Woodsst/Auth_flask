import redis

from config.settings import default_settings


def redis_conn():
    return redis.Redis(
        host=default_settings.redis_host,
        port=default_settings.redis_port,
        db=0,
    )
