from http import HTTPStatus

import pytest

from ..testdata.responses import TOKEN_WRONG_FORMAT
from ..utils.http_requests import registration, login, get_access_token
from ..testdata.data_for_test import USERS, LOGIN, OUT_TIME_TOKEN, TOKEN_URL


def test_update_tokens_200(http_con, clear_databases):
    """Проверка обновления токенов по refresh токену"""

    registration(http_con, USERS[0])
    tokens = login(http_con, LOGIN)

    response = http_con.get(
        f"{TOKEN_URL}token",
        headers={"Authorization": tokens.get("result").get("refresh-token")},
    )
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert len(response_data) == 2
    assert response_data.get("access-token") != tokens.get("access-token")
    assert response_data.get("refresh-token") != tokens.get("refresh-token")


def test_update_tokens_401(http_con, clear_databases):
    """Проверка ответа при передаче не корректного токена"""

    response = http_con.get(
        f"{TOKEN_URL}token", headers={"Authorization": "bad_token"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    message = response.json()
    assert message == TOKEN_WRONG_FORMAT


def test_check_token_200(http_con, clear_databases):
    """Проверка состояния токенов"""

    token = get_access_token(http_con)

    response = http_con.get(
        f"{TOKEN_URL}/check", headers={"Authorization": token}
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "token, http_status",
    [
        ("Bad Token", HTTPStatus.UNAUTHORIZED),
        (OUT_TIME_TOKEN, HTTPStatus.UNAUTHORIZED),
    ],
)
def test_check_token_401(http_con, token, http_status):
    """Ошибки проверки состояния токенов"""

    response = http_con.get(
        f"{TOKEN_URL}/check", headers={"Authorization": token}
    )
    assert response.status_code == http_status

    message = response.json()
    assert message == TOKEN_WRONG_FORMAT
