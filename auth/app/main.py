from flask import Flask
from auth.app.api.v1.hello import hello_page
from auth.app.db.postgres.alchemy_init import init_db


app = Flask(__name__)

app.register_blueprint(hello_page)


def main():
    init_db(app)
    app.run()


if __name__ == '__main__':
    main()
