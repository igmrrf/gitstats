from ...common.db import db


class Insight(db.Model):
    # __tablename__ = "insight"
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.Text, nullable=False)

    def __repre__(self) -> str:
        return f"{self.page} with date view"

    def get_id(self):
        return self.id
