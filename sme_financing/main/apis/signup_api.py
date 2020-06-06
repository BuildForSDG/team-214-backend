"""RESTful API Client resource."""

from flask import request
from flask_restx import Resource

from ..auth.signup_auth import sign_up_with_email_and_password 
from .dto import SignUpDTO

api = SignUpDTO.signup_api 
_sign_up = SignUpDTO.signup


@api.route("/register")
class Signup(Resource):
    @api.doc("User Register")
    @api.expect(_sign_up, validate=True)
    @api.response(201, "User successfully registered")
    def post(self):
        data = request.json
        return sign_up_with_email_and_password(email=data['email'],password=data['password'])

