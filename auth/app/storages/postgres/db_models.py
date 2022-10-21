import uuid
from sqlalchemy.dialects.postgresql import UUID
from storages.postgres.alchemy_init import db


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
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    r_jwt = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    social = db.relationship("UserSocial")

    def __repr__(self):
        return f"<User {self.login}>"


class UserSocial(db.Model):
    __tablename__ = "user_social"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    client_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    social_id = db.Column(db.ForeignKey("social.id"), primary_key=True)
    url = db.Column(db.String)
    social = db.relationship("Social")


class Social(db.Model):
    __tablename__ = "social"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.Integer, nullable=False)


def init_tables(app):
    """Создание таблиц если их нет"""

    app.app_context().push()
    db.create_all()
