import logging
from logging.config import dictConfig


dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format":
                    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "filename": "all_messages.log",
            },
            "console": {"class": "logging.StreamHandler", "level": "WARNING"},
        },
        "root": {"level": "INFO", "handlers": ["wsgi", "file", "console"]},
    }
)


logger = logging.getLogger(__name__)
