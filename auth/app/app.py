from flask import Flask

app = Flask(__name__)
from storages.db_connect import postgres_init, redis_init

postgres_init(app)
redis_init()

from core.models import spec

spec.register(app)

from api.v1.crud import crud_pages
from api.v1.login import login_page
from api.v1.profile import profile
from api.v1.registration import registration_page
from api.v1.tokens_work import tokens_work

app.register_blueprint(tokens_work)
app.register_blueprint(registration_page)
app.register_blueprint(login_page)
app.register_blueprint(profile)
app.register_blueprint(crud_pages)
