"""RESTful API Client resource."""

from flask import request
from flask_restx import Resource

from ..auth.login_auth import login_with_email_and_password
from .dto import LoginDTO

api = LoginDTO.login_api
_login = LoginDTO.login


@api.route("/login")
class Login(Resource):
    @api.doc("User login")
    @api.expect(_login, validate=True)
    @api.response(201, "User successfully registered")
    def post(seldf):
        data = request.json
        return login_with_email_and_password(data=data)
