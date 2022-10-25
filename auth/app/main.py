from api.v1.tokens_work import tokens_work
from api.v1.login import login_page
from api.v1.registration import registration_page
from api.v1.profile import profile
from config.logger import logger
from config.settings import default_settings
from flask import Flask
from storages.db_connect import init_db

app = Flask(__name__)

app.register_blueprint(tokens_work)
app.register_blueprint(registration_page)
app.register_blueprint(login_page)
app.register_blueprint(profile)


def main():
    init_db()
    logger.info("app start")
    app.run(host=default_settings.host_app, debug=default_settings.debug)


if __name__ == "__main__":
    main()
