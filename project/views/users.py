from flask_restx import Resource, Namespace
from flask import request

from project.dao.models import User
from project.schemas.users import UserSchema
from project.services import user_service
from project.setup_db import db

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def post(self):
        data = User().load(request.json)
        new_user = user_service.create_user(**data)
        return new_user, 201

@user_ns.route('/<uid: int>')
class UserView(Resource):
    def get(self,uid):
        user=user_service.get_one(uid)
        sel_user=UserSchema().dump(user)
        return sel_user, 200
    def put(self, uid):
        update_user= user_service.filter_by(uid).update(request.json)
        return UserSchema().dump(update_user)
    def patch(self,uid):
        user = user_service.filter_by(uid).partially_update(request.json)
        return user, 204
