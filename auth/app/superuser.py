import uuid

import sqlalchemy.exc
from email_validator import validate_email

from core.defaultrole import DefaultRole
from storages.db_connect import db
from storages.postgres.db_models import User


def add_admin(login: str, password: str, email: str):
    """Запись администратора в базу"""

    validate_email(email)
    if len(password) < 8:
        raise ValueError("password too short")
    try:
        user_id = uuid.uuid4()
        user = User(
            login=login,
            password=password,
            email=email,
            id=user_id,
            role=DefaultRole.ADMIN_KEY.value,
        )
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        print("user exists")
