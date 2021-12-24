from flask_restx import Resource, Namespace
from flask import request

from project.dao.models import User
from project.services import user_service
from project.setup_db import db

user_ns = Namespace('user')


@user_ns.route('/')
class UsersView(Resource):
    def post(self):
        data = User().load(request.json)
        new_user = user_service.create_user(**data)
        return new_user, 201

@user_ns.route('/')
class UserView(Resource):
