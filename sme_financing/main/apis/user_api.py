from flask import request
from flask_restx import Resource

from ..service.user_service import get_all_users, get_user_by_public_id, save_user
from .dto import UserDTO

api = UserDTO.user_api
_user = UserDTO.user
_userList = UserDTO.userList


@api.route("/")
class UserList(Resource):
    @api.doc("list of users")
    @api.marshal_list_with(_userList, envelope="data")
    def get(self):
        """List all users."""
        return get_all_users()

    @api.doc("create a new user")
    @api.expect(_user, validate=True)
    @api.response(201, "User successfully created")
    def post(self):
        """Creates a new user."""
        data = request.json
        return save_user(data=data)


@api.route("/<public_id>")
@api.param("public_id", "The user identifier")
@api.response(404, "User not found")
class User(Resource):
    @api.doc("get a user")
    @api.marshal_with(_user)
    def get(self, public_id):
        """Get a user given its public_id."""
        user = get_user_by_public_id(public_id)
        if not user:
            api.abort(404)
        else:
            return user
