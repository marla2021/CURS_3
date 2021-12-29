
from project.dao import UserDAO
from project.exceptions import ItemNotFound, NotValidPassword
from project.schemas.users import UserSchema
from project.services.base import BaseService
from project.tools.security import compare_password

class UsersService(BaseService):
    def get_one(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)


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
        if not compare_password(user.password,old_password):
            raise NotValidPassword
        UserDAO(self._db_session).update_by_password(user_id, new_password)

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