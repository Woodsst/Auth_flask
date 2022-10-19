from auth.app.db.postgres.alchemy_init import db
from auth.app.db.postgres.db_models import User


def ss():
    # Insert-запросы
    admin = User(login="admin", password="password")
    db.session.add(admin)
    db.session.commit()

    # Select-запросы
    User.query.all()
    User.query.filter_by(login="admin").first()
