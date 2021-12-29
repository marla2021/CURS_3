
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

    def create(self, email, password):
        user = User(email=email, password= generate_password_hash(password))
        self._db_session.add(user)
        try:
            self._db_session.commit()
        except Exception:
            raise DuplicateError
        return user


    def update(self, uid):
        user = self.get_by_id(uid)
        user.name = user.get("name")
        user.emaile = user.get("email")
        user.password = user.get("password")
        user.surname = user.get("surname")
        user.favorite_genre = user.get("favorite_genre")

        self.session.add(user)
        self.session.commit()

    def update_by_password(self, user_id,password):
        user = User.query.get(user_id)
        user.password = generate_password_hash(password)
        self._db_session.add(user)
        self._db_session.commit()



