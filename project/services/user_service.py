import base64
import hashlib
import hmac
from project.config import BaseConfig
from project.dao import UserDAO
from project.exceptions import ItemNotFound, NotValidPassword
from project.schemas.users import UserSchema
from project.services.base import BaseService
from project.dao.models.user import User

class UsersService(BaseService):
    def get_one(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def partially_update(self, uid):
        user = self.get_by_id(uid)
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


    def create_user(self, email, password):
        user = UserDAO(self._db_session).create(email, password)
        return UserSchema().dump(user)


    def change_password(self,user_id, old_password, new_password):
        user = UserDAO(self._db_session).get_by_id(user_id)
        if not user:
            raise ItemNotFound
        if not compare_passwords(user.password,old_password):
            raise NotValidPassword
        UserDAO(self._db_session).update_by_password(user_id, new_password)