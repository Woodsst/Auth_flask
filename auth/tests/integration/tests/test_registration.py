import json
from http import HTTPStatus

import pytest

from ..testdata.data_for_test import USERS, REGISTRATION_URL, CONTENT_TYPE
from ..testdata.responses import (
    REGISTRATION_COMPLETE,
    REGISTRATION_FAILED,
)


def test_registration_200(clear_databases, http_con):
    """Проверка регистрации клиента"""

    response = http_con.post(
        REGISTRATION_URL,
        data=json.dumps(USERS[0]),
        headers=CONTENT_TYPE,
    )

    assert response.status_code == HTTPStatus.CREATED
    message = response.json()
    assert message == REGISTRATION_COMPLETE


def test_registration_401(http_con, clear_databases):
    """Проверка ошибки регистрации при уже существующем клиенте"""

    http_con.post(
        REGISTRATION_URL, data=json.dumps(USERS[0]), headers=CONTENT_TYPE
    )
    response = http_con.post(
        REGISTRATION_URL, data=json.dumps(USERS[0]), headers=CONTENT_TYPE
    )
    assert response.status_code == HTTPStatus.CONFLICT

    response = response.json()
    assert response == REGISTRATION_FAILED


@pytest.mark.parametrize(
    "bad_request, status_code",
    [
        (
            {
                "url": REGISTRATION_URL,
                "data": json.dumps(
                    {
                        "login": "",
                        "password": "asdasdsssada",
                        "email": "lupa@gmail.com",
                    },
                ),
                "headers": CONTENT_TYPE,
            },
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
        (
            {
                "url": REGISTRATION_URL,
                "data": json.dumps(
                    {
                        "login": "pupa",
                        "password": "",
                        "email": "lupa@gmail.com",
                    },
                ),
                "headers": CONTENT_TYPE,
            },
            HTTPStatus.UNPROCESSABLE_ENTITY,
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
                "headers": CONTENT_TYPE,
            },
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_registration_400(http_con, clear_databases, bad_request, status_code):
    """Проверка ошибок валидации логина пароля и почты"""
    response = http_con.post(**bad_request)
    assert response.status_code == status_code
