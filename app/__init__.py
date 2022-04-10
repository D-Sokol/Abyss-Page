import os
from dotenv import load_dotenv
from flask import Flask

from .routes import basic_bp, admin_bp
from .models import db
from .feedback import mail

load_dotenv()


class Config:
    HOST = os.getenv("HOST", "localhost")
    PORT = os.getenv("PORT", "5000")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///app.db").replace(
        "postgres://", "postgresql://", 1
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = os.getenv("MAIL_PORT", "465")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = (os.getenv("MAIL_USE_TLS", "false") == "true")
    MAIL_USE_SSL = (os.getenv("MAIL_USE_SSL", "true") == "true")

    UNIVERSAL_PAGE = os.getenv("UNIVERSAL_PAGE", "/")
    FEEDBACK_FREQ = int(os.getenv("FEEDBACK_FREQ", 600))

    DEBUG = (os.getenv("DEBUG", "false") == "true")
    SECRET = os.getenv("SECRET", "42")
    SECRET_KEY = os.getenv("SECRET_KEY")
    assert DEBUG or SECRET != "42", "You should use non-default secret in a production deployment"


def create_app(config: Config) -> Flask:
    app = Flask(__name__, static_url_path="/")
    app.config.from_object(config)
    app.register_blueprint(basic_bp)
    app.register_blueprint(admin_bp)

    db.init_app(app)
    db.create_all(app=app)

    mail.init_app(app)
    return app
