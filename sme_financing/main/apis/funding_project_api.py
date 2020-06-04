from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from ..service import funding_project_service as service
from .dto import FundingProjectDTO

api = FundingProjectDTO.funding_project_api
_funding_project = FundingProjectDTO.funding_project


@api.route("/")
class FundingProjectList(Resource):
    @api.doc("list of funding projects")
    @api.marshal_list_with(_funding_project, envelope="data")
    def get(self):
        """List all funding projects."""
        return service.get_all_funding_projects()

    @api.doc("Create a new funding project")
    @api.expect(_funding_project, validate=True)
    @api.response(HTTPStatus.NOT_FOUND, "Investor not found")
    @api.response(HTTPStatus.NOT_FOUND, "Funding application not found")
    @api.response(201, "Funding project successfully registered")
    def post(self):
        """Create a new funding project."""
        data = request.json
        return service.create_funding_project(data=data)


@api.route("/<funding_project_number>")
@api.param("funding_project_number", "Funding project number to process")
class FundingProjectByID(Resource):
    @api.doc("Get a single funding project")
    @api.marshal_with(_funding_project)
    def get(self, funding_project_number):
        """Retrieve a funding project by number."""
        funding_project = service.get_funding_project_by_number(funding_project_number)
        if not funding_project:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding project not found"
            )
        else:
            return funding_project

    @api.doc("Delete an Investor")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete the Investor")
    def delete(self, funding_project_number):
        """Delete an Investor."""
        funding_project = service.get_funding_project_by_number(funding_project_number)
        if not funding_project:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding project not found"
            )
        else:
            return service.delete_funding_project(funding_project)

    @api.doc("Update a Funding project")
    @api.expect(_funding_project, validate=True)
    @api.response(HTTPStatus.CREATED, "Funding project successfully updated")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't update the Funding project")
    def patch(self, funding_project_number):
        """Update a Funding project."""
        funding_project = service.get_funding_project_by_number(funding_project_number)
        if not funding_project:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding project not found"
            )
        else:
            data = request.json
            return service.update_funding_project(data, funding_project)
