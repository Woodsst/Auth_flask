import datetime
import json
from http import HTTPStatus

import pytest

from ..testdata.data_for_test import USERS, LOGIN, LOGIN_URL, \
    ACCESS_TOKEN_LIFE_TIME, REFRESH_TOKEN_LIFE_TIME, LOGOUT_URL, PROFILE_URL
from ..utils.http_requests import registration, get_access_token
from ..utils.jwt_api import decode_access_token, decode_refresh_token


def test_login_200(http_con, clear_databases):
    """Проверка входа в аккаунт и возвращаемых токенов"""

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

    assert ACCESS_TOKEN_LIFE_TIME > int(time_for_exited) > 0

    refresh_token = tokens.get("refresh-token")

    payload = decode_refresh_token(refresh_token)

    assert len(payload) == 5
    assert payload.get("token") == "refresh"

    end_time = payload["end_time"]
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    time_for_exited = (
            end_time.timestamp() - datetime.datetime.utcnow().timestamp()
    )

    assert REFRESH_TOKEN_LIFE_TIME > int(time_for_exited) > 0


@pytest.mark.parametrize(
    "body, status_code", [
        ({"login": "", "password": ""}, HTTPStatus.BAD_REQUEST),
        ({}, HTTPStatus.BAD_REQUEST),
        ({"login": "asd", "password": "sss"}, HTTPStatus.BAD_REQUEST),
        ({"login": "user1", "password": "sss"}, HTTPStatus.BAD_REQUEST),
    ]
)
def test_login_400(http_con, clear_databases, status_code, body):
    """Проверка ошибок при входе пользователя"""
    registration(http_con, USERS[0])

    http_con.request("POST", LOGIN_URL, body=json.dumps(body))
    assert http_con.getresponse().status == status_code


def test_logout_200(http_con, clear_databases):
    """Проверка выхода пользователя из аккаунта"""

    token = get_access_token(http_con)

    http_con.request("GET", LOGOUT_URL, headers={"Authorization": token})
    response = http_con.getresponse()

    assert response.status == HTTPStatus.OK

    http_con.request("GET", PROFILE_URL, headers={"Authorization": token})
    response = http_con.getresponse()
    assert response.status == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    "token, status_code", [
        ("bad token", HTTPStatus.BAD_REQUEST),
        ("", HTTPStatus.BAD_REQUEST)
    ]
)
def test_logout_400(http_con, clear_databases, token, status_code):
    """Проверка невалидного токена для выхода из аккаунта"""

    http_con.request("GET", LOGOUT_URL, headers={"Authorization": token})
    response = http_con.getresponse()

    assert response.status == HTTPStatus.BAD_REQUEST
