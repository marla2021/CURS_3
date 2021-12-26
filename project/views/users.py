from flask_restx import Resource, Namespace
from flask import request

from project.dao.models import User
from project.schemas.users import UserSchema
from project.services import user_service
from project.helpers import auth_required

users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):
    def post(self):
        data = User().load(request.json)
        new_user = user_service.create_user(**data)
        return new_user, 201

@users_ns.route('/<uid: int>')
class UserView(Resource):
    @auth_required
    def get(self,uid):
        user=user_service.get_one(uid)
        sel_user=UserSchema().dump(user)
        return sel_user, 200


    @auth_required
    def patch(self,uid):
        user = user_service.filter_by(uid).partially_update(request.json)
        return user, 204


@users_ns.route('/password')
class UserViewPut(Resource):
    @auth_required
    def put(self,uid, old_pass, new_pass):
        user= user_service.get_one(uid)
        if old_pass == user.password:
            old_pass = new_pass
        self.dao.update