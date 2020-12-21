import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///secret_number.sqlite"))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    secret_number = db.Column(db.Integer)
    attempts = db.Column(db.Integer)
    games_played = db.Column(db.Integer)
    session_token = db.Column(db.String)