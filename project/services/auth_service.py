from project.dao import UserDAO
from project.schemas.users import UserSchema
from project.services.base import BaseService
from project.tools.security import compare_password
from project.tools.tokens import JWTTokens


class AuthService(BaseService):

    def create(self, email, password):
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise Exception
        if not compare_password(user.password, password):
            raise Exception
        data = UserSchema().dump(user)
        return JWTTokens().generate_tokens(data)


    def regenerate_tokens(self, refresh_token, access_token):
        data = JWTTokens().decode_token(refresh_token)
        return JWTTokens().generate_tokens(data)