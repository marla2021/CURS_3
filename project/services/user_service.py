import base64
import hashlib
import hmac
from project.config import BaseConfig
from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.users import UserSchema
from project.services.base import BaseService


class UsersService(BaseService):
    def get_item_by_id(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def partially_update(self, uid):
        user = self.get_item_by_id(uid)
        if "name" in user:
            user.name = user.get("name")
        if "surname" in user:
            user.surname = user.get("surname")
        if "favorite_genre" in user:
            user.surname = user.get("favorite_genre")
        self.users_service.update(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def create_user(self, user_d):
        return self.dao.create(user_d)

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