from flask import Blueprint
from flask_restx import Api

from .apis.client_api import api as client_ns
from .apis.document_api import api as document_ns
from .apis.fund_disbursement_api import api as disburse_ns
from .apis.funding_application_api import api as funding_ns
from .apis.funding_criteria_api import api as funding_criteria_ns
from .apis.funding_project_api import api as funding_project_ns
from .apis.investor_api import api as investor_ns
from .apis.login_api import api as login_ns
from .apis.reset_password_api import api as reset_ns
from .apis.signup_api import api as signup_ns
from .apis.sme_api import api as sme_ns
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
rest_api.add_namespace(investor_ns, path="/investors")
rest_api.add_namespace(sme_ns, path="/smes")
rest_api.add_namespace(document_ns, path="/documents")
rest_api.add_namespace(funding_ns, path="/funding")
rest_api.add_namespace(funding_criteria_ns, path="/funding-criteria")
rest_api.add_namespace(funding_project_ns, path="/funding-projects")
rest_api.add_namespace(login_ns, path="/login")
rest_api.add_namespace(signup_ns, path="/register")
rest_api.add_namespace(reset_ns, path="/reset")
rest_api.add_namespace(disburse_ns, path="/disburse")
# rest_api.add_namespace(fund_detail_ns, path="/fund-detail")
