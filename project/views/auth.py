from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import ValidationError

from project.setup_db import db
from project.exceptions import DecodeError

from project.schemas.users import  UserValidatorSchema, JWTTokensValidatore
from project.services import AuthService, UsersService

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthViewLogin(Resource):
    def post(self):
        try:
            data = UserValidatorSchema().load(request.json)
            return AuthService(db.session).create(**data),201
        except ValidationError as e:
            abort(message=str(e)), 404

    def put(self):
        try:
            current_tokens =JWTTokensValidatore().load(request.json)
            return AuthService(db.session).regenerate_tokens(current_tokens), 200
        except DecodeError:
            abort(404, "Invalid refresh token")



@auth_ns.route('/register')
class AuthViewRegister(Resource):
    def post(self):
        try:
            data = UserValidatorSchema().load(request.json)
            new_user = UsersService(db.session).create_user(**data)
            return new_user
        except ValidationError as e:
            abort(message=str(e)), 404