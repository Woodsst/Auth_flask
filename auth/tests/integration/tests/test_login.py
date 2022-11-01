import datetime
import json
from http import HTTPStatus

import pytest

from ..testdata.data_for_test import (
    USERS,
    LOGIN,
    LOGIN_URL,
    ACCESS_TOKEN_LIFE_TIME,
    REFRESH_TOKEN_LIFE_TIME,
    LOGOUT_URL,
    PROFILE_URL,
)
from ..testdata.responses import (
    LOGOUT,
)
from ..utils.http_requests import registration, get_access_token
from ..utils.jwt_api import decode_access_token, decode_refresh_token


def test_login_200(http_con, clear_databases):
    """Проверка входа в аккаунт и возвращаемых токенов"""

    registration(http_con, USERS[0])

    response = http_con.post(
        LOGIN_URL,
        data=json.dumps(LOGIN),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == HTTPStatus.OK

    tokens = response.json().get("result")

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
    "body, status_code",
    [
        ({"login": "", "password": ""}, HTTPStatus.UNAUTHORIZED),
        ({}, HTTPStatus.UNPROCESSABLE_ENTITY),
        (
            {"login": "asd", "password": "sss"},
            HTTPStatus.UNAUTHORIZED,
        ),
        (
            {"login": "user1", "password": "sss"},
            HTTPStatus.UNAUTHORIZED,
        ),
    ],
)
def test_login_400(http_con, clear_databases, status_code, body):
    """Проверка ошибок при входе пользователя"""
    registration(http_con, USERS[0])

    response = http_con.post(
        LOGIN_URL,
        data=json.dumps(body),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == status_code


def test_logout_200(http_con, clear_databases):
    """Проверка выхода пользователя из аккаунта"""

    token = get_access_token(http_con)

    response = http_con.get(LOGOUT_URL, headers={"Authorization": token})

    assert response.status_code == HTTPStatus.OK

    assert response.json() == LOGOUT

    response = http_con.get(PROFILE_URL, headers={"Authorization": token})
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    "token, status_code",
    [
        ("badtoken", HTTPStatus.UNPROCESSABLE_ENTITY),
        ("", HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
def test_logout_422(http_con, clear_databases, token, status_code):
    """Проверка невалидного токена для выхода из аккаунта"""

    response = http_con.get(LOGOUT_URL, headers={"Authorization": token})

    assert response.status_code == status_code
