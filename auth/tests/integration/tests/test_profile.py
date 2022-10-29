import json
from http import HTTPStatus

import pytest

from ..testdata.data_for_test import USERS, LOGIN, USER_AGENT, PROFILE_URL
from ..utils.http_requests import get_access_token
from ..testdata.responses import (
    TOKEN_WRONG_FORMAT,
    EMAIL_CHANGE,
    WRONG_EMAIL,
    PASSWORD_CHANGE,
    SHORT_PASSWORD,
)


def test_profile_data_200(http_con, clear_databases):
    """Проверка получаемых данных при запросе данных профиля"""
    access_token = get_access_token(http_con)

    http_con.request(
        "GET", PROFILE_URL, headers={"Authorization": access_token}
    )

    response = http_con.getresponse()
    assert response.status == HTTPStatus.OK

    response_data = json.loads(response.read())

    assert len(response_data) == 3
    assert isinstance(response_data, dict)
    assert response_data.get("login") == LOGIN.get("login")
    assert response_data.get("email") == USERS[0].get("email")
    assert response_data.get("role") == "User"


def test_profile_data_401(http_con, clear_databases):
    """Проверка доступа к профилю по невалидному токену"""

    access_token = "bad token"
    http_con.request(
        "GET", PROFILE_URL, headers={"Authorization": access_token}
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.UNAUTHORIZED
    message = json.loads(response.read())
    assert message == TOKEN_WRONG_FORMAT


def test_profile_devices_200(http_con, clear_databases):
    """Проверка получаемых данных
    при запросе устройств с которых был вход в профиль"""
    access_token = get_access_token(http_con)
    http_con.request(
        "GET",
        f"{PROFILE_URL}devices",
        headers={"Authorization": access_token},
    )

    response = http_con.getresponse()
    assert response.status == HTTPStatus.OK

    response_data = json.loads(response.read())

    assert isinstance(response_data, list)
    first_device = response_data[0]
    assert isinstance(first_device, dict)
    assert len(first_device) == 2
    assert first_device.get("device") == USER_AGENT.get("user-agent")


def test_profile_devices_401(http_con, clear_databases):
    """Проверка доступа к получению устройств в профиле"""
    access_token = "bad token"
    http_con.request(
        "GET",
        f"{PROFILE_URL}devices",
        headers={"Authorization": access_token},
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.UNAUTHORIZED
    message = json.loads(response.read())
    assert message == TOKEN_WRONG_FORMAT


def test_profile_change_email_200(http_con, clear_databases):
    """Проверка работы смены почты клиента"""

    access_token = get_access_token(http_con)
    new_email = "iaimnew@gmail.com"
    http_con.request(
        "POST",
        f"{PROFILE_URL}change/email",
        headers={"Authorization": access_token},
        body=json.dumps({"new_email": new_email}),
    )

    response = http_con.getresponse()
    assert response.status == HTTPStatus.OK

    message = json.loads(response.read())
    assert message == EMAIL_CHANGE

    http_con.request(
        "GET", PROFILE_URL, headers={"Authorization": access_token}
    )

    response_data = json.loads(http_con.getresponse().read())
    assert response_data.get("email") == new_email


def test_profile_change_email_401(http_con):
    """Проверка доступа к функционалу смены почты в профиле пользователя"""

    access_token = "bad token"
    http_con.request(
        "POST",
        f"{PROFILE_URL}change/email",
        headers={"Authorization": access_token},
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.UNAUTHORIZED

    message = json.loads(response.read())
    assert message == TOKEN_WRONG_FORMAT


@pytest.mark.parametrize(
    "bad_email, response_status",
    [
        ("", HTTPStatus.BAD_REQUEST),
        ("asda", HTTPStatus.BAD_REQUEST),
        ("asda@asdas", HTTPStatus.BAD_REQUEST),
    ],
)
def test_profile_change_email_400(
    http_con, bad_email, response_status, clear_databases
):
    """Проверка передачи не валидных адресов почты"""

    access_token = get_access_token(http_con)
    http_con.request(
        "POST",
        f"{PROFILE_URL}change/email",
        headers={"Authorization": access_token},
        body=json.dumps({"new_email": bad_email}),
    )
    response = http_con.getresponse()
    assert response.status == response_status

    message = json.loads(response.read())
    assert message == WRONG_EMAIL


def test_profile_change_password_200(http_con, clear_databases):
    """Проверка функционала смены пароля пользователя"""

    access_token = get_access_token(http_con)

    http_con.request(
        "POST",
        f"{PROFILE_URL}change/password",
        headers={"Authorization": access_token},
        body=json.dumps(
            {
                "password": USERS[0].get("password"),
                "new_password": "iamnewpassword",
            }
        ),
    )

    response = http_con.getresponse()

    assert response.status == HTTPStatus.OK

    response_data = json.loads(response.read())
    assert response_data == PASSWORD_CHANGE


def test_profile_change_password_401(http_con):
    """Проверка доступа к функционалу смены пароля в профиле пользователя"""

    access_token = "bad token"
    http_con.request(
        "POST",
        f"{PROFILE_URL}change/password",
        headers={"Authorization": access_token},
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    "bad_password, response_status, user_password",
    [
        ("", HTTPStatus.BAD_REQUEST, USERS[0].get("password")),
        ("asda", HTTPStatus.BAD_REQUEST, USERS[0].get("password")),
        ("asssssda", HTTPStatus.BAD_REQUEST, "wrong_password"),
    ],
)
def test_profile_change_password_400(
    http_con, user_password, bad_password, response_status, clear_databases
):
    """Проверка передачи не валидных паролей и
    неправильного пароля пользователя"""

    access_token = get_access_token(http_con)
    http_con.request(
        "POST",
        f"{PROFILE_URL}change/password",
        headers={"Authorization": access_token},
        body=json.dumps(
            {"password": user_password, "new_password": bad_password}
        ),
    )
    response = http_con.getresponse()
    assert response.status == response_status
    response_message = json.loads(response.read())
    assert response_message == SHORT_PASSWORD
