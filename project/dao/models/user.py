from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))
    favorite_genre = db.Column(db.String(100), db.ForeignKey("genres.id"))

    def __repr__(self):
        return f"<User '{self.name.title()}'>"