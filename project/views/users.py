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
    def get(self, user_id:int):
        try:
            return UsersService(db.session).get_one(user_id)
        except ItemNotFound:
            abort(404, "User not found")

@users_ns.route('/<int:user_id>')
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
    def put(self,old_pass, new_pass):
        req_json = request.json
        pass