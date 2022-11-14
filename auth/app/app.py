from flask import Flask

from config.settings import settings

app = Flask(__name__)

if settings.tracer:
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from core.jaeger_tracer import configure_tracer
    configure_tracer()
    FlaskInstrumentor().instrument_app(app)

from storages.db_connect import postgres_init, redis_init
from config.limiter import limiter_init

postgres_init(app)
redis_init()
limiter_init(app)


from core.spec_core import spec

spec.register(app)

from api.v1.crud import crud_pages
from api.v1.login import login_page
from api.v1.profile import profile
from api.v1.registration import registration_page
from api.v1.tokens_work import tokens_work
from core.superuser import add_admin

app.register_blueprint(tokens_work)
app.register_blueprint(registration_page)
app.register_blueprint(login_page)
app.register_blueprint(profile)
app.register_blueprint(crud_pages)


@app.cli.command("createadmin")
def create_admin():
    """Команда для добавления пользователя с ролью администратора"""

    login = input("Name: ")
    password = input("Password: ")
    email = input("Email:")

    add_admin(login, password, email)
