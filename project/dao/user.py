
from project.dao.base import BaseDAO
from project.dao.models import User
from project.exceptions import DuplicateError
from project.tools.security import generate_password_hash


class UserDAO(BaseDAO):

    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, **data):
        try:
            user_d = User(**data)
            self._db_session.add(user_d)
            self._db_session.commit()
            return user_d
        except Exception:
            raise DuplicateError


    def partially_update(self, user_id, name=None, surname=None, favorite_genre=None):
        user = self.get_by_id(user_id)
        if name:
            user.name = name
        if surname:
            user.surname = surname
        if favorite_genre:
            user.favorite_genre = favorite_genre
        self._db_session.add(user)
        self._db_session.commit()

    def update_by_password(self, user_id, password):
        user = self.get_by_id(user_id)
        user.password = generate_password_hash(password)
        self._db_session.add(user)
        self._db_session.commit()
