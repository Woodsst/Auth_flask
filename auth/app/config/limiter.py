from typing import Optional

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config.settings import settings

limiter: Optional[Limiter] = None


def limiter_init(app: Flask):
    global limiter
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        storage_uri=(
            f"redis://{settings.redis.host}:" f"{settings.redis.port}"
        ),
        strategy="fixed-window",
    )
