import datetime
import uuid
from copy import copy

from sqlalchemy import UniqueConstraint, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from storages.db_connect import db
from storages.postgres.base import DeviceType, LoginHistoryMixin
from sqlalchemy.sql.ddl import DDL


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(
        db.ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False
    )
    email = db.Column(db.String, nullable=False, unique=True)

    social = relationship("UserSocial", cascade="all, delete")
    device = relationship("UserDevice", cascade="all, delete")
    roles = relationship("Role")

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
    social = relationship("Social", cascade="all, delete")


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
    device = relationship("Device", cascade="all, delete")


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    device = db.Column(db.String, nullable=False)


class Role(db.Model):
    __tablename__ = "roles"

    role_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)


class LoginHistory(LoginHistoryMixin, db.Model):

    __tablename__ = "login_history"
    __table_args__ = (
        UniqueConstraint("id", "device_type"),
        {
            "postgresql_partition_by": "LIST (device_type)",
        },
    )


class LoginHistorySmartphone(LoginHistoryMixin, db.Model):

    __tablename__ = "login_history_mobile"


class LoginHistoryPhablet(LoginHistoryMixin, db.Model):

    __tablename__ = "login_history_pc"


PARTITION_TABLES_REGISTRY = (
    (LoginHistorySmartphone, DeviceType.MOBILE),
    (LoginHistoryPhablet, DeviceType.PC),
)


def create_table_login_history_partition_ddl(
    table: str, device_type: DeviceType
) -> None:
    return DDL(
        """
        ALTER TABLE login_history ATTACH PARTITION %s FOR VALUES IN ('%s');"""
        % (table, device_type.name)
    ).execute_if(dialect="postgresql")


def attach_event_listeners() -> None:
    for class_, device_type in PARTITION_TABLES_REGISTRY:
        class_.__table__.add_is_dependent_on(LoginHistory.__table__)
        event.listen(
            class_.__table__,
            "after_create",
            create_table_login_history_partition_ddl(
                class_.__table__, device_type
            ),
        )


attach_event_listeners()
