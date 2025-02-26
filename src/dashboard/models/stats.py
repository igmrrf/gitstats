from src.common.db import db


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    language = db.Column(db.String(50))
    lines_of_code = db.Column(db.Integer)
    rating = db.Column(db.Float)
    repositories_count = db.Column(db.Integer)
