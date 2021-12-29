
import calendar

from datetime import datetime, timedelta

from flask import request
from flask_restx import abort
import jwt

from project.config import BaseConfig
from project.dao import UserDAO
from project.dao.models.user import User
from project.schemas.users import UserSchema
from project.services import user_service
from project.setup_db import db
from project.tools.security import compare_password
from project.tools.tokens import JWTTokens


class AuthService:

    def create(self, email, password):
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise Exception
        if not compare_password(user.password, password):
            raise Exception
        data = UserSchema().dump(user)
        return JWTTokens().generate_tokens(data)


    def update(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        try:
            data = jwt.decode(jwt=refresh_token, key=BaseConfig.SECRET_KEY, algorithms=[algo])
        except Exception as e:
            abort(400)

        email = data.get("email")

        user = db.session.query(User).filter(User.email == email).first()

        data = {
            "username": user.username,
            "role": user.role
        }
        min = datetime.datetime.utcnow() + datetime.timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
        data["exp"] = calendar.timegm(min.timetuple())
        access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=algo)
        days = datetime.datetime.utcnow() + datetime.timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
        data["exp"] = calendar.timegm(days.timetuple())
        refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201