import datetime
import uuid
from copy import copy
from enum import Enum
from tkinter import EventType

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr
from storages.db_connect import db


class DeviceType(Enum):
    PC = 'pc'
    MOBILE = 'mobile'


class LoginHistoryMixin:

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    @declared_attr
    def user_id(self):
        return db.Column(
            UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE")
        )

    event_type = db.Column(db.Enum(EventType))
    user_agent = db.Column(db.String, nullable=True)
    device_type = db.Column(db.Enum(DeviceType), primary_key=True)
    login_ip = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Login history {self.id}>"

    def as_value(self) -> str:
        return self.event_type.value

    def to_dict(self):
        d = copy(self.__dict__)
        d.pop("_sa_instance_state")
        return d
