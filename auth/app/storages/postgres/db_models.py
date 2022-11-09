import datetime
import uuid
from copy import copy
import datetime
from sqlalchemy import UniqueConstraint


from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from storages.db_connect import db


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


def create_partition(target, connection, **kw) -> None:
    """ creating partition by user_sign_in """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_pc" PARTITION OF "users_sign_in" FOR VALUES IN ('pc')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_mobile" PARTITION OF "users_sign_in" FOR VALUES IN ('mobile')"""
    )


class UserSignIn(db.Model):
    __tablename__ = 'users_sign_in'
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create', create_partition)],
        }
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    logged_in_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_agent = db.Column(db.Text)
    user_device_type = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.logged_in_at }>'
