from project.dao.models.base import BaseMixin
from project.setup_db import db


class Movie(BaseMixin, db.Model):
    __tablename__ = "movies"

    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    trailer = db.Column(db.String(100), unique=True, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float,nullable=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"), nullable=True)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"), nullable=True)

    def __repr__(self):
        return f"<Movie '{self.title.title()}'>"
