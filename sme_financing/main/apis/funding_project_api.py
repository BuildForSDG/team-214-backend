from flask import request
from flask_restx import Resource, reqparse
from flask_restx._http import HTTPStatus
from werkzeug.datastructures import FileStorage

from ..service import funding_detail_service as fd_service
from ..service import funding_project_service as fp_service
from .dto import FundingDetailDTO, FundingProjectDTO

api = FundingProjectDTO.funding_project_api
_funding_project = FundingProjectDTO.funding_project
_funding_detail = FundingDetailDTO.funding_detail

_funding_detail_parser = reqparse.RequestParser()
_funding_detail_parser.add_argument(
    "title", required=True, type=str, help="Funding detail title", location="form"
)
_funding_detail_parser.add_argument(
    "description",
    required=True,
    type=str,
    help="Funding detail description",
    location="form",
)
_funding_detail_parser.add_argument(
    "document_name", type=str, help="Document name", location="form"
)
_funding_detail_parser.add_argument("file", type=FileStorage, location="files")


@api.route("/")
class FundingProjectList(Resource):
    @api.doc("list of funding projects")
    @api.marshal_list_with(_funding_project, envelope="data")
    def get(self):
        """List all funding projects."""
        return fp_service.get_all_funding_projects()

    @api.doc("Create a new funding project")
    @api.expect(_funding_project, validate=True)
    @api.response(HTTPStatus.NOT_FOUND, "Investor not found")
    @api.response(HTTPStatus.NOT_FOUND, "Funding application not found")
    @api.response(201, "Funding project successfully registered")
    def post(self):
        """Create a new funding project."""
        data = request.json
        return fp_service.create_funding_project(data=data)


@api.route("/<funding_project_number>")
@api.param("funding_project_number", "Funding project number to process")
class FundingProjectByID(Resource):
    @api.doc("Get a single funding project")
    @api.marshal_with(_funding_project)
    def get(self, funding_project_number):
        """Retrieve a funding project by number."""
        funding_project = fp_service.get_funding_project_by_number(
            funding_project_number
        )
        if not funding_project:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding project not found"
            )
        else:
            return funding_project

    @api.doc("Delete an funding project")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete the funding project")
    def delete(self, funding_project_number):
        """Delete an funding project."""
        funding_project = fp_service.get_funding_project_by_number(
            funding_project_number
        )
        if not funding_project:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding project not found"
            )
        else:
            return fp_service.delete_funding_project(funding_project)

    @api.doc("Update a Funding project")
    @api.expect(_funding_project, validate=True)
    @api.response(HTTPStatus.CREATED, "Funding project successfully updated")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't update the Funding project")
    def patch(self, funding_project_number):
        """Update a Funding project."""
        funding_project = fp_service.get_funding_project_by_number(
            funding_project_number
        )
        if not funding_project:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding project not found"
            )
        else:
            data = request.json
            return fp_service.update_funding_project(data, funding_project)


@api.route("/<funding_project_number>/funding_details")
@api.param("funding_project_number", "Funding project number to process")
@api.response(HTTPStatus.NOT_FOUND, "Funding detail not found")
class FundingProjectDetail(Resource):
    @api.doc("list of funding details of a funding project")
    @api.marshal_list_with(_funding_detail, envelope="data")
    def get(self, funding_project_number):
        """
        List all funding details of a funding project.
        """
        return fp_service.get_project_funding_details(funding_project_number)

    @api.doc("Add funding detail")
    @api.expect(_funding_detail_parser, validate=True)
    @api.response(HTTPStatus.NOT_FOUND, "Funding project not found")
    @api.response(201, "Funding detail successfully added")
    def post(self, funding_project_number):
        """Add a funding detail."""
        funding_project = fp_service.get_funding_project_by_number(
            funding_project_number
        )
        if not funding_project:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding project not found"
            )
        else:
            data = _funding_detail_parser.parse_args()
            if not data["title"] or not data["description"]:
                self.api.abort(
                    code=HTTPStatus.NOT_FOUND, message="Empty inputs",
                )
            else:
                return fd_service.create_funding_detail(data, funding_project)


@api.route("/<funding_project_number>/funding_details/<funding_detail_id>")
@api.param("funding_project_number", "Funding project number to process")
@api.param("funding_detail_id", "Funding detail ID to process")
@api.response(HTTPStatus.NOT_FOUND, "Funding detail not found")
class FundingProjectDetailByID(Resource):
    @api.doc("Remove funding detail")
    @api.response(HTTPStatus.NOT_FOUND, "Funding project not found")
    @api.response(201, "Funding detail successfully added")
    def delete(self, funding_project_number, funding_detail_id):
        """Remove funding detail."""
        funding_project = fp_service.get_funding_project_by_number(
            funding_project_number
        )
        if not funding_project:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding project not found"
            )
        funding_detail = fd_service.get_funding_detail_by_id(funding_detail_id)
        if not funding_detail:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding detail not found"
            )
        return fp_service.remove_funding_detail(funding_project, funding_detail)


# @api.route("/<funding_project_number>/project_milestones")
# @api.param("funding_project_number", "Funding project number to process")
# @api.response(HTTPStatus.NOT_FOUND, "Funding detail not found")
# class FundingProjectMilestones(Resource):
#     @api.doc("list of project milestones of a funding project")
#     @api.marshal_list_with(_funding_milestone, envelope="data")
#     def get(self, funding_project_number):
#         """
#         List all project milestones of a funding project.
#         """
#         return fp_service.get_project_project_milestones(funding_project_number)


# @api.route("/<funding_project_number>/fund_disbursements")
# @api.param("funding_project_number", "Funding project number to process")
# @api.response(HTTPStatus.NOT_FOUND, "Fund disbursements not found")
# class FundingProjectFundDisbursement(Resource):
#     @api.doc("list of fund disbursements of a funding project")
#     @api.marshal_list_with(_fund_disbursement, envelope="data")
#     def get(self, funding_project_number):
#         """
#         List all fund disbursements of a funding project.
#         """
#         return fp_service.get_project_fund_disbursements(funding_project_number)
