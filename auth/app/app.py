from flask import Flask, request

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from jaeger_tracer import configure_tracer

configure_tracer()

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)

from storages.db_connect import postgres_init, redis_init

postgres_init(app)
redis_init()

from core.spec_core import spec

spec.register(app)

from api.v1.crud import crud_pages
from api.v1.login import login_page
from api.v1.profile import profile
from api.v1.registration import registration_page
from api.v1.tokens_work import tokens_work
from superuser import add_admin

app.register_blueprint(tokens_work)
app.register_blueprint(registration_page)
app.register_blueprint(login_page)
app.register_blueprint(profile)
app.register_blueprint(crud_pages)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')


@app.cli.command("createadmin")
def create_admin():
    """Команда для добавления пользователя с ролью администратора"""

    login = input("Name: ")
    password = input("Password: ")
    email = input("Email:")

    add_admin(login, password, email)
