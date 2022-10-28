import json
from http import HTTPStatus

import pytest
from ..utils.http_requests import (
    login,
    add_new_role,
    registration,
    get_access_token,
)
from ..testdata.data_for_test import (
    ADMIN_LOGIN,
    CRUD_URL,
    NEW_ROLE,
    DESCRIPTION,
    USERS,
    PROFILE_URL,
)
from ..utils.db_requests import registration_admin, get_user_id


def test_add_role_200(http_con, clear_databases, postgres_con):
    """Проверка добавления новой роли и её описания"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token['access-token']}"

    add_new_role(http_con, token)

    response = http_con.getresponse()

    assert response.status == HTTPStatus.OK

    http_con.request(
        "GET", f"{CRUD_URL}roles", headers={"Authorization": token}
    )

    response = json.loads(http_con.getresponse().read())

    assert isinstance(response, dict)
    assert len(response) == 3
    assert response.get(NEW_ROLE) == DESCRIPTION


@pytest.mark.parametrize(
    "role, description, status_code",
    [
        ("", "", HTTPStatus.BAD_REQUEST),
        ("", "asd", HTTPStatus.BAD_REQUEST),
        ("a", "asd", HTTPStatus.BAD_REQUEST),
    ],
)
def test_add_role_400(
    http_con, postgres_con, role, description, status_code, clear_databases
):
    """Проверка передачи невалидных ролей и описаний,
    а так же повторения ролей"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token['access-token']}"

    http_con.request(
        "POST",
        f"{CRUD_URL}add_role",
        body=json.dumps({"role": role, "description": description}),
        headers={"Authorization": token},
    )

    assert http_con.getresponse().status == status_code


def test_delete_role_200(http_con, postgres_con, clear_databases):
    """Проверка удаления роли, при удалении роли,
    если роль была у пользователей, их роль меняется на User"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token['access-token']}"

    add_new_role(http_con, token)
    http_con.getresponse()
    registration(http_con, USERS[0])
    user_id = get_user_id(postgres_con)

    http_con.request(
        "POST",
        f"{CRUD_URL}set_user_role",
        body=json.dumps({"role": NEW_ROLE, "user_id": user_id}),
        headers={"Authorization": token},
    )
    http_con.getresponse()

    http_con.request(
        "POST",
        f"{CRUD_URL}delete_role",
        body=json.dumps({"role": NEW_ROLE}),
        headers={"Authorization": token},
    )
    response = http_con.getresponse()
    assert response.status == HTTPStatus.OK

    http_con.request(
        "GET", f"{CRUD_URL}roles", headers={"Authorization": token}
    )
    response_data = json.loads(http_con.getresponse().read())
    assert response_data.get(NEW_ROLE) is None
    token = login(http_con, USERS[0])
    token = f"Bearer {token['access-token']}"

    http_con.request("GET", PROFILE_URL, headers={"Authorization": token})
    response_data = json.loads(http_con.getresponse().read())

    assert response_data.get("role") == "User"


@pytest.mark.parametrize(
    "role, status_code",
    [
        ("", HTTPStatus.BAD_REQUEST),
        ("Admin", HTTPStatus.BAD_REQUEST),
        ("User", HTTPStatus.BAD_REQUEST),
    ],
)
def test_delete_role_400(
    postgres_con, http_con, clear_databases, role, status_code
):
    """Проверка невалидных запросов"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token['access-token']}"

    http_con.request(
        "POST",
        f"{CRUD_URL}delete_role",
        body=json.dumps({"role": role}),
        headers={"Authorization": token},
    )

    response = http_con.getresponse()
    assert response.status == status_code


def test_change_role_200(postgres_con, http_con, clear_databases):
    """Проверка изменения роли и описания"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token['access-token']}"
    add_new_role(http_con, token)
    http_con.getresponse()
    change_role = "change_role"
    change_desc = "change_description"
    http_con.request(
        "POST",
        f"{CRUD_URL}change_role",
        body=json.dumps(
            {
                "role": NEW_ROLE,
                "change_role": change_role,
                "change_description": change_desc,
            }
        ),
        headers={"Authorization": token},
    )

    response = http_con.getresponse()
    assert response.status == HTTPStatus.OK

    http_con.request(
        "GET", f"{CRUD_URL}roles", headers={"Authorization": token}
    )
    response_data = json.loads(http_con.getresponse().read())
    assert response_data.get(change_role) == change_desc


@pytest.mark.parametrize(
    "role, desc, status_code",
    [
        ("Admin", "", HTTPStatus.BAD_REQUEST),
        ("User", "", HTTPStatus.BAD_REQUEST),
        (None, "", HTTPStatus.BAD_REQUEST),
        ("", None, HTTPStatus.BAD_REQUEST),
    ],
)
def test_change_role_400(
    postgres_con, http_con, clear_databases, role, desc, status_code
):
    """Проверка невалидных запросов на изменение роли и описания"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token['access-token']}"
    add_new_role(http_con, token)
    http_con.getresponse()

    http_con.request(
        "POST",
        f"{CRUD_URL}change_role",
        body=json.dumps(
            {"role": NEW_ROLE, "change_role": role, "change_description": desc}
        ),
        headers={"Authorization": token},
    )

    response = http_con.getresponse()
    assert response.status == status_code


def test_set_user_role_200(http_con, postgres_con, clear_databases):
    """Проверка изменения роли пользователя"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token['access-token']}"

    add_new_role(http_con, token)
    http_con.getresponse()
    registration(http_con, USERS[0])
    user_id = get_user_id(postgres_con)

    http_con.request(
        "POST",
        f"{CRUD_URL}set_user_role",
        body=json.dumps({"role": NEW_ROLE, "user_id": user_id}),
        headers={"Authorization": token},
    )
    response = http_con.getresponse()

    assert response.status == HTTPStatus.OK
    token = login(http_con, USERS[0])
    token = f"Bearer {token['access-token']}"

    http_con.request("GET", PROFILE_URL, headers={"Authorization": token})
    response_data = json.loads(http_con.getresponse().read())

    assert response_data.get("role") == NEW_ROLE


@pytest.mark.parametrize(
    "user_id, role, status_code",
    [
        ("", "", HTTPStatus.BAD_REQUEST),
        (None, "", HTTPStatus.BAD_REQUEST),
        ("", None, HTTPStatus.BAD_REQUEST),
    ],
)
def test_set_user_role_400(
    http_con, postgres_con, clear_databases, role, user_id, status_code
):
    """Проверка не валидных запросов изменения роли пользователя"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token['access-token']}"

    http_con.request(
        "POST",
        f"{CRUD_URL}set_user_role",
        body=json.dumps({"role": role, "user_id": user_id}),
        headers={"Authorization": token},
    )
    response = http_con.getresponse()

    assert response.status == status_code


def test_get_all_roles(http_con, postgres_con, clear_databases):
    """Проверка получения списка всех ролей"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token['access-token']}"

    http_con.request(
        "GET", f"{CRUD_URL}roles", headers={"Authorization": token}
    )
    response = http_con.getresponse()

    assert response.status == HTTPStatus.OK
    response_data = json.loads(response.read())
    assert len(response_data) == 2
    assert response_data.get("Admin") == "full access"
    assert response_data.get("User") == "default access"


def test_get_add_roles_400(http_con, postgres_con, clear_databases):
    """Проверка запроса без доступа для получения списка всех ролей"""

    token = get_access_token(http_con)

    http_con.request(
        "GET", f"{CRUD_URL}roles", headers={"Authorization": token}
    )
    response = http_con.getresponse()

    assert response.status == HTTPStatus.FORBIDDEN
