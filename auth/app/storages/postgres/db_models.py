import uuid
from main import app
from sqlalchemy.dialects.postgresql import UUID
from storages.postgres.alchemy_init import db, init_db


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
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    r_jwt = db.Column(db.String, nullable=False)

    roles = db.relationship("Role")

    def __repr__(self):
        return f"<User {self.login}>"


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User {self.role}>"


# Инстанс таблиц в базу
init_db(app)
app.app_context().push()
db.create_all()
# Создание ролей

if Role.query.count() == 0:
    follower = Role(id=1, role="follower")
    subscriber = Role(id=2, role="subscriber")
    db.session.add(follower)
    db.session.add(subscriber)
    db.session.commit()
