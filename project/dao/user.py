import base64
import hashlib
import hmac


from project.config import BaseConfig
from project.dao.base import BaseDAO
from project.dao.models import User
from project.schemas.users import UserSchema


class UserDAO(BaseDAO):

    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, data):
        user_schema = UserSchema()
        user_dict = user_schema.load(data)
        user = User(**user_dict)
        self.session.add(user)
        self.session.commit()
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

    def update_by_password(self):
        pass

