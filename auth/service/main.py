from flask import Flask
from endpoints.hello import hello_page


app = Flask(__name__)

app.register_blueprint(hello_page)

if __name__ == '__main__':
    app.run()
