from flask_restx import Resource, Namespace
from flask import request, abort

from project.exceptions import ItemNotFound
from project.setup_db import db
from project.schemas.users import UserSchema
from project.services import user_service, UsersService
from project.helpers import auth_required

users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):
    def get(self):
        try:
            return UsersService(db.session).get_all_users()
        except ItemNotFound:
            abort(404, "User not found")

    @auth_required
    def get(self,user_id):
        user = UsersService(db.session).get_one(user_id)
        sel_user = UserSchema().dump(user)
        return sel_user, 200

    @auth_required
    def patch(self,user_id):
        user = UsersService(db.session).partially_update(request.json)
        return user, 204


@users_ns.route('/password')
class UserViewPut(Resource):
    @auth_required
    def put(self, user_id, old_password, new_password):
        try:
            user = UsersService(db.session).change_password(user_id, old_password,new_password)
            return "", 204
        except ValueError as e:
            abort(404, message=str(e))