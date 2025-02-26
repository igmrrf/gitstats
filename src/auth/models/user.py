from flask_login import UserMixin

from src.common.db import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(100), unique=True)
    access_token = db.Column(db.String(100))
    profile_url = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return f"<User {self.username}>"
