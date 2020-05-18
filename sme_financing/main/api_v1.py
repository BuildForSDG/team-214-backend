from flask import Blueprint
from flask_restx import Api

from .apis.client_api import api as client_ns
from .apis.user_api import api as user_ns

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
rest_api = Api(
    blueprint,
    version="1.0",
    title="SME financing APIs v1",
    description="APIS",
    doc="/docs",
)

rest_api.add_namespace(user_ns, path="/users")
rest_api.add_namespace(client_ns, path="/clients")
