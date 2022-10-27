import datetime
import sys
import uuid
from copy import copy

import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
from storages.db_connect import Base, db_session
from exceptions import LoginException
from config.logger import logger


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False, unique=True)
    role = Column(
        ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False
    )
    email = Column(String, nullable=False, unique=True)

    @validates("login", "password")
    def validate_login(self, key, field) -> str:
        if key == "login":
            if len(field) <= 2:
                raise LoginException()
        return field

    social = relationship("UserSocial", cascade="all, delete")
    device = relationship("UserDevice", cascade="all, delete")
    roles = relationship("Role")

    def __repr__(self):
        return f"<User {self.login}>"

    def to_dict(self):
        d = copy(self.__dict__)
        d.pop("_sa_instance_state")
        return d


class UserSocial(Base):
    __tablename__ = "user_social"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    social_id = Column(
        ForeignKey("socials.id", ondelete="CASCADE"), primary_key=True
    )
    url = Column(String, nullable=False, unique=True)
    social = relationship("Social", cascade="all, delete")


class Social(Base):
    __tablename__ = "socials"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class UserDevice(Base):
    __tablename__ = "user_device"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    device_id = Column(
        ForeignKey("devices.id", ondelete="CASCADE"), primary_key=True
    )
    entry_time = Column(DateTime, default=datetime.datetime.utcnow())
    device = relationship("Device", cascade="all, delete")


class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    device = Column(String, nullable=False)


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)


def added_default_roles():
    try:
        if len(Role.query.all()) > 0:
            return
        admin = Role(role="Admin", description="full access")
        user = Role(role="User", description="default access")
        db_session.add(admin)
        db_session.add(user)
        db_session.commit()
    except sqlalchemy.exc.ProgrammingError:
        logger.warn("app start without migrations!")
        sys.exit(1)
