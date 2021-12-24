import base64
import hashlib
import hmac

from flask_restx import abort

from project.config import BaseConfig
from project.dao.base import BaseDAO
from project.dao.models import User


class UserDAO(BaseDAO):

    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        data_for_check = User.get_by_email(user_d.email)
        if user_d["email"] == data_for_check:
            abort(405)

        self.session.add(ent)
        self.session.commit()
        return ent

    def get_hash(password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            BaseConfig.PWD_HASH_SALT,
            BaseConfig.PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def compare_passwords(self, get_hash, password):
        return hmac.compare_digest(
            base64.b64decode(get_hash),
            hashlib.pbkdf2_hmac('sha256', password.encode(), BaseConfig.PWD_HASH_SALT, BaseConfig.PWD_HASH_ITERATIONS))

    def update(self, uid):
        user = self.get_item_by_id(uid)
        user.name = user.get("name")
        user.emaile = user.get("email")
        user.password = user.get("password")
        user.surname = user.get("surname")
        user.favorite_genre = user.get("favorite_genre")

        self.session.add(user)
        self.session.commit()
