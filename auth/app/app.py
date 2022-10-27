from flask import Flask

from api.v1.crud import crud_pages
from api.v1.login import login_page
from api.v1.profile import profile
from api.v1.registration import registration_page
from api.v1.tokens_work import tokens_work
from config.logger import logger
from config.settings import default_settings
from storages.postgres.db_models import added_default_roles

app = Flask(__name__)

app.register_blueprint(tokens_work)
app.register_blueprint(registration_page)
app.register_blueprint(login_page)
app.register_blueprint(profile)
app.register_blueprint(crud_pages)
added_default_roles()


def main():
    added_default_roles()
    logger.info("app start")
    app.run(host=default_settings.host_app, debug=default_settings.debug)


if __name__ == "__main__":
    main()
