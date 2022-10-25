import datetime
import uuid
from copy import copy

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from sqlalchemy_utils.types.choice import ChoiceType
from storages.db_connect import db
from exceptions import LoginException


class User(db.Model):
    __tablename__ = "users"

    ROLES = [
        ("user", "User"),
        ("subscriber", "Subscriber"),
        ("admin", "Admin"),
    ]

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(ChoiceType(ROLES), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    @validates("login", "password")
    def validate_login(self, key, field) -> str:
        if key == "login":
            if len(field) <= 2:
                raise LoginException()
        return field

    social = db.relationship("UserSocial", cascade="all, delete")
    device = db.relationship("UserDevice", cascade="all, delete")

    def __repr__(self):
        return f"<User {self.login}>"

    def to_dict(self):
        d = copy(self.__dict__)
        d.pop("_sa_instance_state")
        return d


class UserSocial(db.Model):
    __tablename__ = "user_social"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(
        db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    social_id = db.Column(
        db.ForeignKey("socials.id", ondelete="CASCADE"), primary_key=True
    )
    url = db.Column(db.String, nullable=False, unique=True)
    social = db.relationship("Social", cascade="all, delete")


class Social(db.Model):
    __tablename__ = "socials"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


class UserDevice(db.Model):
    __tablename__ = "user_device"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(
        db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    device_id = db.Column(
        db.ForeignKey("devices.id", ondelete="CASCADE"), primary_key=True
    )
    entry_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    device = db.relationship("Device", cascade="all, delete")


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    device = db.Column(db.String, nullable=False)


def init_tables(app):
    """Создание таблиц если их нет"""

    app.app_context().push()
    db.create_all()
