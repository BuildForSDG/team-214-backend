"""RESTful API Client resource"""

from flask import request
from flask_restx import Resource

from ..service.client_service import (
    get_all_clients,
    get_client_by_email,
    get_client_by_user_id,
    save_client,
)
from .dto import ClientDTO

api = ClientDTO.client_api
_client = ClientDTO.client


@api.route("/")
class ClientList(Resource):
    @api.doc("list of clients")
    @api.marshal_list_with(_client, envelope="data")
    def get(self):
        """List all clients."""
        return get_all_clients()

    @api.doc("create a new client")
    @api.expect(_client, validate=True)
    @api.response(201, "Client successfully registered")
    def post(self):
        """Creates a new client."""
        data = request.json
        return save_client(data=data)


@api.route("/user/<user_id>")
@api.param("user_id", "The user id")
@api.response(404, "Client not found")
class ClientUser(Resource):
    @api.doc("get a client based on its user_id")
    @api.marshal_with(_client)
    def get(self, user_id):
        """Get a client given its user_id."""
        client = get_client_by_user_id(user_id)
        if not client:
            api.abort(404)
        else:
            return client


@api.route("/email/<email>")
@api.param("email", "The client email")
@api.response(404, "Client not found")
class Client(Resource):
    @api.doc("get a client based on its email")
    @api.marshal_with(_client)
    def get(self, email):
        """Get a client given its email."""
        client = get_client_by_email(email)
        if not client:
            api.abort(404)
        else:
            return client
