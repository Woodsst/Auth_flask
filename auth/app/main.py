from flask import Flask
from api.v1.hello import hello_page
from db.postgres.alchemy_init import init_db
from config.settings import default_settings

app = Flask(__name__)

app.register_blueprint(hello_page)


def main():
    init_db(app)
    app.run(host=default_settings.host_app,
            debug=default_settings.debug)


if __name__ == "__main__":
    main()
