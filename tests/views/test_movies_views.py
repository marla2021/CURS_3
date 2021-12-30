import pytest

from project.dao.models import Movie


class TestMoviesView:
    url = "/movies/"

    @pytest.fixture
    def movie(self, db):
        g = Movie(title="1Йеллоустоун")
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_movies(self, client, movie):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json == [
            {"id": movie.id,
             "title": movie.title,
             "description": movie.description,
		  	 "trailer": movie.trailer,
			 "year": movie.year,
			 "rating": movie.rating,
			 "genre_id": movie.genre_id,
			 "director_id":movie.director_id,},
        ]


class TestMovieView:
    url = "/movies/{movie_id}"

    @pytest.fixture
    def movie(self, db):
        g = Movie(
                 title="Йеллоустоун",
                 description="Владелец ранчо пытается сохранить землю своих предков",
                 trailer="https://www.youtube.com/watch?v=UKei_d0cbP4",
                 year=2018,
                 rating=8.6,
                 genre_id=17,
                 director_id= 1,
                  )
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_movie(self, client, movie):
        response = client.get(self.url.format(movie_id=movie.id))
        assert response.status_code == 200
        assert response.json == {
                                 "id": movie.id,
                                 "title": movie.title,
			                     "description": movie.description,
		                      	 "trailer": movie.trailer,
		                      	 "year": movie.year,
			                     "rating": movie.rating,
			                     "genre_id": movie.genre_id,
			                     "director_id": movie.director_id,
                                 }

    def test_movie_not_found(self, client):
        response = client.get(self.url.format(movie_id=1))
        assert response.status_code == 404
