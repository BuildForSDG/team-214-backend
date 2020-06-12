"""RESTful API Client resource."""

from flask import request
from flask_restx import Resource

from ..auth.login_auth import forget_password
from .dto import ForgetPasswordDTO

api = ForgetPasswordDTO.forget_api
_forget_password = ForgetPasswordDTO.forget_password


@api.route("")
class Signup(Resource):
    @api.doc("User forget password")
    @api.expect(_forget_password, validate=True)
    @api.response(201, "Reset password link sent")
    def post(self):
        data = request.json
        return forget_password(email=data["email"])
