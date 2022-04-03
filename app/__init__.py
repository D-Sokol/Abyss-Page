import os
from dotenv import load_dotenv
from flask import Flask

from .routes import bp
from .models import db

load_dotenv()


class Config:
    HOST = os.getenv("HOST", "localhost")
    PORT = os.getenv("PORT", "5000")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True


def create_app(config: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(bp)
    db.init_app(app)
    db.create_all(app=app)
    return app
