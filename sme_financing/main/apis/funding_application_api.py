"""RESTful FundingApplication resource."""

from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from ..service.funding_application_service import (
    delete_funding_application,
    get_all_funding_applications,
    get_funding_application_by_id,
    save_funding_application,
    update_funding_application,
)
from .dto import FundingApplicationDTO

api = FundingApplicationDTO.funding_api
_funding_application = FundingApplicationDTO.funding_application


@api.route("/funding_applications")
class FundingApplicationResource(Resource):
    @api.doc("list of all funding applications")
    @api.marshal_list_with(_funding_application, envelope="data")
    def get(self):
        """List all funding applications."""
        return get_all_funding_applications()

    @api.doc("Create a new funding application")
    @api.expect(_funding_application, validate=True)
    @api.response(201, "Funding application successfully created")
    def post(self):
        """Create a new funding application."""
        data = request.json
        return save_funding_application(data=data)


@api.route("/funding_applications/<int:funding_application_id>")
@api.param("funding_application_id", "The ID of the Funding Application to process")
@api.response(HTTPStatus.NOT_FOUND, "Funding Application not found")
class FundingApplicationByID(Resource):
    @api.doc("Get a single Funding Application")
    @api.marshal_with(_funding_application)
    def get(self, funding_application_id):
        """Retrieve a Funding Application."""
        funding_application = get_funding_application_by_id(funding_application_id)
        if not funding_application:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding Application not found"
            )
        else:
            return funding_application

    @api.doc("Delete a Funding Application")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete the Funding Application")
    def delete(self, funding_application_id):
        """Delete a Funding Application."""
        funding_application = get_funding_application_by_id(funding_application_id)
        if not funding_application:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding Application not found"
            )
        else:
            return delete_funding_application(funding_application)

    @api.doc("Update a Funding Application")
    @api.expect(_funding_application, validate=True)
    @api.response(HTTPStatus.CREATED, "Funding application successfully updated")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't update the Funding Application")
    @api.response(HTTPStatus.NOT_FOUND, "SME specified doesn't exist")
    def patch(self, funding_application_id):
        """Update a Funding Application."""
        funding_application = get_funding_application_by_id(funding_application_id)
        if not funding_application:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding Application not found"
            )
        else:
            data = request.json
            return update_funding_application(data, funding_application)
