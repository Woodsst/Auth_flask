import argparse
import uuid
from core.defaultrole import DefaultRole
import psycopg2
from email_validator import validate_email
from werkzeug.security import generate_password_hash

from config.settings import default_settings


def add_superuser(user_data: dict):
    """Функция для добавления пользователя"""

    con = psycopg2.connect(default_settings.postgres)
    with con.cursor() as cur:
        cur.execute(
            """
        INSERT INTO users (id, login, password, role, email)
        VALUES (%(id)s, %(login)s, %(password)s, %(role)s, %(email)s)
        """,
            {
                "id": str(uuid.uuid4()),
                "login": user_data["login"],
                "password": generate_password_hash(user_data["password"]),
                "role": DefaultRole.ADMIN_KEY.value,
                "email": user_data["email"],
            },
        )
        con.commit()


parser = argparse.ArgumentParser()
parser.add_argument(
    "createsuperuser",
    help="Команда для создания пользователя с правами администратора",
)

args = parser.parse_args()
if args.createsuperuser:
    name = input("Name: ")
    password = input("Password: ")
    email = input("Email:")
    validate_email(email)
    if len(password) < 8:
        raise ValueError("password too short")
    user_data = {
        "login": name,
        "password": password,
        "email": email,
    }

    add_superuser(user_data)
