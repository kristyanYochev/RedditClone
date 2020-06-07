from flask import Flask
from flask_cors import CORS
from reddit.extensions import api, jwt


def register_extensions(app: Flask):
    api.init_app(app)
    jwt.init_app(app)
    CORS(app)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    register_extensions(app)
    return app
