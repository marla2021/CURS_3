from project.dao.models.base import BaseMixin
from project.setup_db import db


class Movie(BaseMixin, db.Model):
    __tablename__ = "movies"

    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Movie '{self.name.title()}'>"
