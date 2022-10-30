from flasgger import Swagger
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

template = {
  "swagger": "2.0",
  "info": {
    "title": "Cервис Auth",
    "description": ("Сервис Auth создан для авторизации пользователей, а "
                    "так же для управления доступом пользователей"),
  },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, template=template, config=swagger_config)

app.register_blueprint(tokens_work)
app.register_blueprint(registration_page)
app.register_blueprint(login_page)
app.register_blueprint(profile)
app.register_blueprint(crud_pages)
added_default_roles()


def main():
    logger.info("app start")
    app.run(host=default_settings.host_app, debug=default_settings.debug)


if __name__ == "__main__":
    main()
