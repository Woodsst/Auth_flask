import json
from http import HTTPStatus

import pytest

from ..testdata.data_for_test import USERS
from ..testdata.responses import (
    REGISTRATION_COMPLETE,
    WRONG_EMAIL,
    SHORT_PASSWORD,
    REGISTRATION_FAILED,
    WRONG_LOGIN,
)


def test_registration_200(clear_databases, http_con):
    """Проверка регистрации клиента"""

    http_con.request(
        "POST",
        "/api/v1/registration",
        body=json.dumps(USERS[0]),
        headers={"user-agent": "python"},
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.CREATED
    message = json.loads(response.read())
    assert message == REGISTRATION_COMPLETE


def test_registration_401(http_con, clear_databases):
    """Проверка ошибки регистрации при уже существующем клиенте"""

    http_con.request(
        "POST",
        "/api/v1/registration",
        body=json.dumps(USERS[0]),
        headers={"user-agent": "python"},
    )
    http_con.getresponse()
    http_con.request(
        "POST",
        "/api/v1/registration",
        body=json.dumps(USERS[0]),
        headers={"user-agent": "python"},
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.CONFLICT
    response = json.loads(response.read())
    assert response == REGISTRATION_FAILED


@pytest.mark.parametrize(
    "bad_request, status_code, response_body",
    [
        (
            {
                "method": "POST",
                "url": "/api/v1/registration",
                "body": json.dumps(
                    {
                        "login": "",
                        "password": "asdasdsssada",
                        "email": "lupa@gmail.com",
                    }
                ),
                "headers": {"user-agent": "python"},
            },
            HTTPStatus.BAD_REQUEST,
            WRONG_LOGIN,
        ),
        (
            {
                "method": "POST",
                "url": "/api/v1/registration",
                "body": json.dumps(
                    {
                        "login": "pupa",
                        "password": "",
                        "email": "lupa@gmail.com",
                    }
                ),
                "headers": {"user-agent": "python"},
            },
            HTTPStatus.BAD_REQUEST,
            SHORT_PASSWORD,
        ),
        (
            {
                "method": "POST",
                "url": "/api/v1/registration",
                "body": json.dumps(
                    {
                        "login": "pupa",
                        "password": "asdasdaaaaa",
                        "email": "lupagmail.com",
                    }
                ),
                "headers": {"user-agent": "python"},
            },
            HTTPStatus.BAD_REQUEST,
            WRONG_EMAIL,
        ),
    ],
)
def test_registration_400(
    http_con, clear_databases, bad_request, status_code, response_body
):
    """Проверка ошибок валидации логина пароля и почты"""
    http_con.request(**bad_request)
    response = http_con.getresponse()
    assert response.status == status_code
    assert json.loads(response.read()) == response_body
