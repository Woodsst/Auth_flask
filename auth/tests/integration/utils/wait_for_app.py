import logging
import http.client
import backoff

logger = logging.getLogger(__name__)


@backoff.on_exception(
    backoff.expo,
    ConnectionRefusedError,
    max_tries=10,
    max_time=20,
    logger=logger.warning("Пытаемся соединится с приложением"),
)
def connect_app():
    logger.warning("Повторная попытка соединения с приложением")
    con = http.client.HTTPConnection(
        host="flask", port=5000
    )
    con.request("GET", "/api/v1/check")
    con.getresponse()


if __name__ == "__main__":
    connect_app()
