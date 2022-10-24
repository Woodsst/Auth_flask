import json
from http import HTTPStatus

import pytest

from auth.tests.integration.testdata.users import USERS
from auth.tests.integration.utils.db_requests import clear_table


def test_registration_200(postgres_con, http_con):
    http_con.request(
        "POST",
        "/api/v1/registration",
        body=json.dumps(USERS[0]),
        headers={"user-agent": "python"},
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.CREATED
    clear_table(postgres_con)


def test_registration_409(http_con, postgres_con):
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
    assert response.get("error") == "login or email already registered"
    clear_table(postgres_con)


@pytest.mark.parametrize(
    "bad_request, status_code, response_body",
    [
        (
            {
                "method": "POST",
                "url": "/api/v1/registration",
                "body": json.dumps(
                    {
                        "user": {
                            "login": "",
                            "password": "asdasdsssada",
                            "email": "lupa@gmail.com",
                        }
                    }
                ),
                "headers": {"user-agent": "python"},
            },
            HTTPStatus.FORBIDDEN,
            {"error": "login too short"},
        ),
        (
            {
                "method": "POST",
                "url": "/api/v1/registration",
                "body": json.dumps(
                    {
                        "user": {
                            "login": "pupa",
                            "password": "",
                            "email": "lupa@gmail.com",
                        }
                    }
                ),
                "headers": {"user-agent": "python"},
            },
            HTTPStatus.FORBIDDEN,
            {"error": "pass too short"},
        ),
        (
            {
                "method": "POST",
                "url": "/api/v1/registration",
                "body": json.dumps(
                    {
                        "user": {
                            "login": "pupa",
                            "password": "asdasdaaaaa",
                            "email": "lupagmail.com",
                        }
                    }
                ),
                "headers": {"user-agent": "python"},
            },
            HTTPStatus.FORBIDDEN,
            {"error": "The email address is not valid"},
        ),
    ],
)
def test_registration_403(
    http_con, postgres_con, bad_request, status_code, response_body
):
    http_con.request(**bad_request)
    response = http_con.getresponse()
    assert response.status == HTTPStatus.FORBIDDEN
    assert json.loads(response.read()) == response_body
    clear_table(postgres_con)
