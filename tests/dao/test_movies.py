import pytest

from project.dao import MovieDAO
from project.dao.models import Movie


class TestMovieDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = MovieDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        t = Movie(title="rghedht",
                  description="История превращения застенчивого парня Реджинальда Дуайта",
                  trailer="https://youtu.be/VISiqVeKTq8",
                  year=2019,
                  rating=7.9,
                  genre_id=19,
                  director_id=5 )
        db.session.add(t)
        db.session.commit()
        return t

    @pytest.fixture
    def movie_2(self, db):
        g = Movie(title="jo;ljo;",
                  description="Али - молодая амбициозная девушка из маленького городка",
                  trailer="https://www.youtube.com/watch?v=sgOhxneHkiE",
                  year=2010,
                  rating=6.4,
                  genre_id=18,
                  director_id=5)
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_movie_by_id(self, movie_1):
        assert self.dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self):
        assert self.dao.get_by_id(1) is None

    def test_get_all_movies(self, movie_1, movie_2):
        assert self.dao.get_all() == [movie_1, movie_2]