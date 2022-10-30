import json
from http import HTTPStatus

import pytest

from ..testdata.responses import TOKEN_WRONG_FORMAT
from ..utils.http_requests import registration, login, get_access_token
from ..testdata.data_for_test import USERS, LOGIN, OUT_TIME_TOKEN


def test_update_tokens_200(http_con, clear_databases):
    """Проверка обновления токенов по refresh токену"""

    registration(http_con, USERS[0])
    tokens = login(http_con, LOGIN)
    http_con.request(
        "GET",
        "/api/v1/token",
        headers={"Authorization": tokens.get("refresh-token")},
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.OK
    response_data = json.loads(response.read())
    assert isinstance(response_data, dict)
    assert len(response_data) == 2
    assert response_data.get("access-token") != tokens.get("access-token")
    assert response_data.get("refresh-token") != tokens.get("refresh-token")


def test_update_tokens_401(http_con, clear_databases):
    """Проверка ответа при передаче не корректного токена"""

    http_con.request(
        "GET", "/api/v1/token", headers={"Authorization": "bad_token"}
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.UNAUTHORIZED
    message = json.loads(response.read())
    assert message == TOKEN_WRONG_FORMAT


def test_check_token_200(http_con, clear_databases):
    """Проверка состояния токенов"""

    token = get_access_token(http_con)

    http_con.request("GET", "/api/v1/check", headers={"Authorization": token})
    response = http_con.getresponse()
    assert response.status == HTTPStatus.OK


@pytest.mark.parametrize(
    "token, http_status",
    [
        ("Bad Token", HTTPStatus.UNAUTHORIZED),
        (OUT_TIME_TOKEN, HTTPStatus.UNAUTHORIZED),
    ],
)
def test_check_token_401(http_con, token, http_status):
    """Ошибки проверки состояния токенов"""

    http_con.request("GET", "/api/v1/check", headers={"Authorization": token})
    response = http_con.getresponse()
    assert response.status == http_status
    message = json.loads(response.read())
    assert message == TOKEN_WRONG_FORMAT
