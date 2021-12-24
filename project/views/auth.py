from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import ValidationError

from project.schemas.auth import AuthSchema

from project.dao.models import User
from project.schemas.users import UserSchema

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthViewLogin(Resource):
    def post(self):
        try:
            data = AuthSchema().load(request.json)
            tokens = AuthSchema.create(**data)
            return tokens, 201
        except ValidationError as e:
            abort(message=str(e)), 404

    def put(self):
        auth = AuthSchema().load(request.json)
        if auth is None:
            abort(400)
        tokens = AuthSchema.update(request.json)
        return tokens, 201

@auth_ns.route('/register')
class AuthViewRegister(Resource):
    def post(self):
        try:
            data = UserSchema.load(request.json)
            new_user = User(**data)
            return new_user, 201
        except ValidationError as e:
            abort(message=str(e)), 404