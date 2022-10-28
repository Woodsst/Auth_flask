import datetime
import json
from http import HTTPStatus

from ..testdata.data_for_test import USERS, LOGIN, LOGIN_URL
from ..utils.http_requests import registration
from ..utils.jwt_api import decode_access_token, decode_refresh_token


def test_login_200(http_con, clear_databases):
    """Проверка входа в аккаунт"""

    registration(http_con, USERS[0])

    http_con.request("POST", LOGIN_URL, body=json.dumps(LOGIN))

    response = http_con.getresponse()

    assert response.status == HTTPStatus.OK

    tokens = json.loads(response.read())

    assert len(tokens) == 2

    assert isinstance(tokens.get("access-token"), str)
    assert isinstance(tokens.get("refresh-token"), str)

    access_token = tokens.get("access-token")

    payload = decode_access_token(access_token)

    assert len(payload) == 5
    assert payload.get("token") == "access"

    end_time = payload["end_time"]
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    time_for_exited = (
        end_time.timestamp() - datetime.datetime.utcnow().timestamp()
    )

    assert 3600 > int(time_for_exited) > 0

    refresh_token = tokens.get("refresh-token")

    payload = decode_refresh_token(refresh_token)

    assert len(payload) == 5
    assert payload.get("token") == "refresh"

    end_time = payload["end_time"]
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    time_for_exited = (
        end_time.timestamp() - datetime.datetime.utcnow().timestamp()
    )

    assert 1210000 > int(time_for_exited) > 0
