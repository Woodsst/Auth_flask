import uuid
from werkzeug.security import generate_password_hash

from ..testdata.data_for_test import USERS


def clear_table(con):
    """Очистка базы данных"""

    con.cursor().execute(
        "delete from users;"
        "delete from devices;"
        "delete from socials;"
        "delete from roles where role != 'Admin' and role != 'User'"
    )
    con.commit()


def registration_admin(con):
    """Добавление пользователя с правами админа"""

    con.cursor().execute(
        """insert into users(id, login, password, email, role)
        values(%(id)s, %(login)s, %(password)s, %(email)s, %(role)s)""",
        {
            "id": str(uuid.uuid4()),
            "login": "admin",
            "password": generate_password_hash("admin111"),
            "email": "admin@gmail.com",
            "role": 1,
        },
    )
    con.commit()


def get_user_id(con):
    """Получение ид пользователя"""

    login = USERS[0].get("login")
    cur = con.cursor()
    cur.execute(
        """select id from users where login = %(login)s""", {"login": login}
    )
    result = cur.fetchone()[0]
    return result
