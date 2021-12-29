from project.dao.base import BaseDAO
from project.dao.models import Movie
from flask import request


class MovieDAO(BaseDAO):
    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self):
        query_param = request.args
        limit = query_param.get("limit", 12)
        start = query_param.get("start", 0)
        return self._db_session.query(Movie).limit(limit).offset(start).all()
