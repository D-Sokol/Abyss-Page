from flask import Flask
from .routes import bp


class Config:
    host = "localhost"
    port = 5000
    debug = True


def create_app(config: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(bp)
    return app
