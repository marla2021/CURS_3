from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import ValidationError

from project.dao.models.auth import AuthValidator
from project.services.auth_service import auth_service


auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthView(Resource):
    def post(self):
        try:
            data = AuthValidator().load(request.json)
            tokens = auth_service.create(**data)
            return tokens, 201
        except ValidationError as e:
            abort, 404

    def put(self):
        auth = AuthSchema().load(request.json)
        if auth is None:
            abort(400)
        tokens = auth_service.update(request.json)
        return tokens, 201

