from flask import Flask
from api.v1.update_tokens import update
from api.v1.registration import registration_page
from storages.db_connect import init_db
from config.settings import default_settings
from config.logger import logger

app = Flask(__name__)

app.register_blueprint(update)
app.register_blueprint(registration_page)


def main():
    init_db(app)
    logger.info("app start")
    app.run(host=default_settings.host_app, debug=default_settings.debug)


if __name__ == "__main__":
    main()
