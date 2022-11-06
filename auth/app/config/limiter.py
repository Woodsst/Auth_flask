from typing import Optional

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config.settings import default_settings

limiter: Optional[Limiter] = None


def limiter_init(app: Flask):
    global limiter
    limiter = Limiter(
        app, key_func=get_remote_address,
        storage_uri=(f"redis://{default_settings.redis_host}:"
                     f"{default_settings.redis_port}"),
        strategy="fixed-window",
    )
