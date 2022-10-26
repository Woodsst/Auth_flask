import argparse

import sqlalchemy
from werkzeug.security import generate_password_hash

from storages.db_connect import db_session
from storages.postgres.db_models import User
from services.crud import DefaultRole


def add_superuser(user_data: dict):
    try:
        admin = User(
            role=DefaultRole.ADMIN_KEY.value,
            login=user_data["login"],
            password=generate_password_hash(user_data["password"]),
            email=user_data["email"],
        )
        db_session.add(admin)
        db_session.commit()
    except sqlalchemy.exc.IntegrityError:
        print("User already exist")
        return


parser = argparse.ArgumentParser()
parser.add_argument("createsuperuser")

args = parser.parse_args()
if args.createsuperuser:
    name = input("Name: ")
    password = input("Password: ")
    email = input("Email:")

user_data = {
    "login": name,
    "password": password,
    "email": email,
}

add_superuser(user_data)
