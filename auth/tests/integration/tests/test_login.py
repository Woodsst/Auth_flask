import datetime
import json
from http import HTTPStatus

import pytest

from ..testdata.responses import (
    WRONG_LOGIN,
    LOGOUT,
    TOKEN_WRONG_FORMAT,
    BAD_REQUEST,
    USER_NOT_FOUND,
    PASSWORD_NOT_MATCH,
    TOKEN_MISSING,
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

    response = http_con.post(LOGIN_URL, data=json.dumps(LOGIN))

    assert response.status_code == HTTPStatus.OK

    tokens = response.json()

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
        ({}, HTTPStatus.BAD_REQUEST, BAD_REQUEST),
        (
            {"login": "asd", "password": "sss"},
            HTTPStatus.UNAUTHORIZED,
            USER_NOT_FOUND,
        ),
        (
            {"login": "user1", "password": "sss"},
            HTTPStatus.UNAUTHORIZED,
            PASSWORD_NOT_MATCH,
        ),
    ],
)
def test_login_400(http_con, clear_databases, status_code, body, message):
    """Проверка ошибок при входе пользователя"""
    registration(http_con, USERS[0])

    response = http_con.post(LOGIN_URL, data=json.dumps(body))
    assert response.status_code == status_code

    assert response.json() == message


def test_logout_200(http_con, clear_databases):
    """Проверка выхода пользователя из аккаунта"""

    token = get_access_token(http_con)

    response = http_con.get(LOGOUT_URL, headers={"Authorization": token})

    assert response.status_code == HTTPStatus.OK

    assert response.json() == LOGOUT

    response = http_con.get(PROFILE_URL, headers={"Authorization": token})
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    "token, status_code, message",
    [
        ("bad token", HTTPStatus.UNAUTHORIZED, TOKEN_WRONG_FORMAT),
        ("", HTTPStatus.UNAUTHORIZED, TOKEN_MISSING),
    ],
)
def test_logout_400(http_con, clear_databases, token, status_code, message):
    """Проверка невалидного токена для выхода из аккаунта"""

    response = http_con.get(LOGOUT_URL, headers={"Authorization": token})

    assert response.status_code == status_code

    assert response.json() == message
