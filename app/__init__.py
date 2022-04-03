import os
from dotenv import load_dotenv
from flask import Flask

from .routes import bp

load_dotenv()


class Config:
    HOST = os.getenv("HOST", "localhost")
    PORT = os.getenv("PORT", "5000")

    DEBUG = True


def create_app(config: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(bp)
    return app
