import datetime
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    ROLES = [
        ("user", "User"),
        ("subscriber", "Subscriber"),
        ("admin", "Admin"),
    ]

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False, unique=True)
    role = Column(ChoiceType(ROLES), nullable=False)
    email = Column(String, nullable=False, unique=True)

    social = relationship("UserSocial")
    device = relationship("UserDevice")

    def __repr__(self):
        return f"<User {self.login}>"

    def to_dict(self):
        self.__dict__.pop("_sa_instance_state")
        return self.__dict__


class UserSocial(Base):
    __tablename__ = "user_social"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    social_id = Column(ForeignKey("socials.id"), primary_key=True)
    url = Column(String, nullable=False, unique=True)
    social = relationship("Social")


class Social(Base):
    __tablename__ = "socials"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class UserDevice(Base):
    __tablename__ = "user_device"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    device_id = Column(ForeignKey("devices.id"), primary_key=True)
    entry_time = Column(DateTime, default=datetime.datetime.utcnow())
    device = relationship("Device")


class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    device = Column(String, nullable=False)
