from flask_restx import Namespace, fields


class UserDTO:
    user_api = Namespace("user", description="User related operations")
    user = user_api.model(
        "user",
        {
            "email": fields.String(required=True, description="user email address"),
            "username": fields.String(required=True, description="user username"),
            "password": fields.String(required=True, description="user password"),
            "public_id": fields.String(required=False, description="user public id"),
        },
    )
    userList = user_api.model(
        "userList",
        {
            "email": fields.String(required=True, description="user email address"),
            "username": fields.String(required=True, description="user username"),
            "password": fields.String(required=True, description="user password"),
            "public_id": fields.String(required=False, description="user public id"),
            "admin": fields.String(required=False, description="user admin status"),
        },
    )


class ClientDTO:
    client_api = Namespace("client", description="Client related operations")
    client = client_api.model(
        "client",
        {
            "lastname": fields.String(required=True, description="Client lastname"),
            "firstname": fields.String(required=True, description="Client firstname"),
            "gender": fields.String(required=True, description="Client gender"),
            "postal_address": fields.String(
                required=True, description="Client postal address"
            ),
            "residential_address": fields.String(
                required=True, description="Client address"
            ),
            "telephone": fields.String(
                required=True, description="Client telephone number"
            ),
            "nationality": fields.String(
                required=True, description="Client nationality"
            ),
            "education_level": fields.String(
                required=True, description="Client education level"
            ),
            "position": fields.String(
                required=True, description="Client position in the SME"
            ),
            "user": fields.Nested(UserDTO().user),
        },
    )
