import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.types.choice import ChoiceType
from storages.postgres.alchemy_init import db


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

    social = db.relationship("UserSocial")
    device = db.relationship("UserDevice")

    def __repr__(self):
        return f"<User {self.login}>"

    def to_dict(self):
        self.__dict__.pop("_sa_instance_state")
        return self.__dict__


class UserSocial(db.Model):
    __tablename__ = "user_social"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    social_id = db.Column(db.ForeignKey("socials.id"), primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    social = db.relationship("Social")


class Social(db.Model):
    __tablename__ = "socials"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


class UserDevice(db.Model):
    __tablename__ = "user_device"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    device_id = db.Column(db.ForeignKey("devices.id"), primary_key=True)
    entry_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    device = db.relationship("Device")


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    device = db.Column(db.String, nullable=False)


def init_tables(app):
    """Создание таблиц если их нет"""

    app.app_context().push()
    db.create_all()
