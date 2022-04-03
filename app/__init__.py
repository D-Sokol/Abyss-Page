import os
from dotenv import load_dotenv
from flask import Flask

from .routes import basic_bp, admin_bp
from .models import db

load_dotenv()


class Config:
    HOST = os.getenv("HOST", "localhost")
    PORT = os.getenv("PORT", "5000")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.getenv("DEBUG", False)
    SECRET = os.getenv("SECRET", "42")
    assert DEBUG or SECRET != "42", "You should use non-default secret in a production deployment"


def create_app(config: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(basic_bp)
    app.register_blueprint(admin_bp)
    db.init_app(app)
    db.create_all(app=app)
    return app
