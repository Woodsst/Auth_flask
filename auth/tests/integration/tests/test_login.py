import datetime
import json
from http import HTTPStatus

import pytest

from ..testdata.responses import (
    WRONG_LOGIN,
    SHORT_PASSWORD,
    LOGOUT,
    TOKEN_WRONG_FORMAT,
)
from ..testdata.data_for_test import (
    USERS,
    LOGIN,
    LOGIN_URL,
    ACCESS_TOKEN_LIFE_TIME,
    REFRESH_TOKEN_LIFE_TIME,
    LOGOUT_URL,
    PROFILE_URL,
)
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
    "body, status_code, message",
    [
        ({"login": "", "password": ""}, HTTPStatus.BAD_REQUEST, WRONG_LOGIN),
        ({}, HTTPStatus.BAD_REQUEST, WRONG_LOGIN),
        (
            {"login": "asd", "password": "sss"},
            HTTPStatus.BAD_REQUEST,
            SHORT_PASSWORD,
        ),
        (
            {"login": "user1", "password": "sss"},
            HTTPStatus.BAD_REQUEST,
            SHORT_PASSWORD,
        ),
    ],
)
def test_login_400(http_con, clear_databases, status_code, body, message):
    """Проверка ошибок при входе пользователя"""
    registration(http_con, USERS[0])

    http_con.request("POST", LOGIN_URL, body=json.dumps(body))
    response = http_con.getresponse()
    assert response.status == status_code

    response_message = json.loads(response.read())
    assert response_message == message


def test_logout_200(http_con, clear_databases):
    """Проверка выхода пользователя из аккаунта"""

    token = get_access_token(http_con)

    http_con.request("GET", LOGOUT_URL, headers={"Authorization": token})
    response = http_con.getresponse()

    assert response.status == HTTPStatus.OK

    response_message = json.loads(response.read())
    assert response_message == LOGOUT

    http_con.request("GET", PROFILE_URL, headers={"Authorization": token})
    response = http_con.getresponse()
    assert response.status == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    "token, status_code",
    [("bad token", HTTPStatus.BAD_REQUEST), ("", HTTPStatus.BAD_REQUEST)],
)
def test_logout_400(http_con, clear_databases, token, status_code):
    """Проверка невалидного токена для выхода из аккаунта"""

    http_con.request("GET", LOGOUT_URL, headers={"Authorization": token})
    response = http_con.getresponse()

    assert response.status == HTTPStatus.BAD_REQUEST

    response_message = json.loads(response.read())
    assert response_message == TOKEN_WRONG_FORMAT
