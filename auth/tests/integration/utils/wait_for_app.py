import logging
import backoff
import requests

logger = logging.getLogger(__name__)


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.ConnectionError,
    max_tries=10,
    max_time=20,
    logger=logger.warning("Пытаемся соединится с приложением"),
)
def connect_app():
    logger.warning("Повторная попытка соединения с приложением")
    con = requests.Session()
    con.get("http://flask:5000/api/v1/check", headers={"X-request-Id": 'asd'})


if __name__ == "__main__":
    connect_app()
