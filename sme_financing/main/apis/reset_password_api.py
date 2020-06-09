"""RESTful API Client resource."""

from flask import request
from flask_restx import Resource

from ..auth.login_auth import reset_password
from .dto import ResetPasswordDTO

api = ResetPasswordDTO.reset_password_api
_reset_password = ResetPasswordDTO.reset_password


@api.route("/")
class Login(Resource):
    @api.doc("Reset user password")
    @api.expect(_reset_password, validate=True)
    @api.response(201, "User password reset successfully")
    def post(self):
        data = request.json
        return reset_password(
            id=data["id"],
            data={
                "password": data["password"],
                "confirmpassword": data["confirmpassword"],
            },
        )
