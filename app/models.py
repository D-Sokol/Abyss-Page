from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    agent = db.Column(db.String(80), nullable=False)
    params = db.Column(db.String(80))
