import json
from http import HTTPStatus

import pytest

from ..testdata.data_for_test import USERS, REGISTRATION_URL
from ..testdata.responses import (
    REGISTRATION_COMPLETE,
    WRONG_EMAIL,
    SHORT_PASSWORD,
    REGISTRATION_FAILED,
    WRONG_LOGIN,
)


def test_registration_200(clear_databases, http_con):
    """Проверка регистрации клиента"""

    response = http_con.post(
        REGISTRATION_URL,
        data=json.dumps(USERS[0]),
    )

    assert response.status_code == HTTPStatus.CREATED
    message = response.json()
    assert message == REGISTRATION_COMPLETE


def test_registration_401(http_con, clear_databases):
    """Проверка ошибки регистрации при уже существующем клиенте"""

    http_con.post(REGISTRATION_URL, data=json.dumps(USERS[0]))
    response = http_con.post(REGISTRATION_URL, data=json.dumps(USERS[0]))
    assert response.status_code == HTTPStatus.CONFLICT

    response = response.json()
    assert response == REGISTRATION_FAILED


@pytest.mark.parametrize(
    "bad_request, status_code, response_data",
    [
        (
            {
                "url": REGISTRATION_URL,
                "data": json.dumps(
                    {
                        "login": "",
                        "password": "asdasdsssada",
                        "email": "lupa@gmail.com",
                    }
                ),
            },
            HTTPStatus.BAD_REQUEST,
            WRONG_LOGIN,
        ),
        (
            {
                "url": REGISTRATION_URL,
                "data": json.dumps(
                    {
                        "login": "pupa",
                        "password": "",
                        "email": "lupa@gmail.com",
                    }
                ),
            },
            HTTPStatus.BAD_REQUEST,
            SHORT_PASSWORD,
        ),
        (
            {
                "url": REGISTRATION_URL,
                "data": json.dumps(
                    {
                        "login": "pupa",
                        "password": "asdasdaaaaa",
                        "email": "lupagmail.com",
                    }
                ),
            },
            HTTPStatus.BAD_REQUEST,
            WRONG_EMAIL,
        ),
    ],
)
def test_registration_400(
    http_con, clear_databases, bad_request, status_code, response_data
):
    """Проверка ошибок валидации логина пароля и почты"""
    response = http_con.post(**bad_request)
    assert response.status_code == status_code
    assert response.json() == response_data
