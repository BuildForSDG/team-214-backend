from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from ..service.funding_criteria_service import (
    delete_funding_criteria,
    get_all_funding_criteria,
    get_funding_criteria_by_id,
    save_funding_criteria,
    update_funding_criteria,
)
from .dto import FundingDTO

api = FundingDTO.funding_api
_funding_criteria = FundingDTO.funding_criteria
_funding_criteria_display = FundingDTO.funding_criteria_display


@api.route("/funding_criteria")
class fundingCriteriaResource(Resource):
    @api.doc("List all funding criteria")
    @api.marshal_list_with(_funding_criteria_display, envelope="data")
    def get(self):
        """
        List all funding criteria
        """
        return get_all_funding_criteria()

    @api.doc("Create a new funding criteria")
    @api.expect(_funding_criteria, validate=True)
    @api.response(201, "Funding criteria successfully created")
    def post(self):
        """
        Create a new funding criteria
        """
        data = request.json
        return save_funding_criteria(data=data)


@api.route("/funding_criteria/<int:funding_criteria_id>")
@api.param("funding_criteria_id", "The ID of the Funding criteria to process")
@api.response(HTTPStatus.NOT_FOUND, "Funding criteria  not found")
class FundingCriteriaById(Resource):
    @api.doc("Get a single funding criteria")
    @api.marshal_with(_funding_criteria_display)
    def get(self, funding_criteria_id):
        """
        Retrieve funding criteria for the given Id
        """
        funding_criteria = get_funding_criteria_by_id(funding_criteria_id)

        if not funding_criteria:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding criteria  not found"
            )
        else:
            return funding_criteria

    @api.doc("Delete funding criteria")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete the Funding Criteria")
    def delete(self, funding_criteria_id):
        """
        Delete the funding criteria by the given Id to delete it
        """
        funding_criteria = get_funding_criteria_by_id(funding_criteria_id)
        if not funding_criteria:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding criteria not found"
            )
        else:
            return delete_funding_criteria(funding_criteria)

    @api.doc("Update a funding criteria")
    @api.expect(_funding_criteria, validate=True)
    @api.response(HTTPStatus.CREATED, "Funding criteria  successfully updated")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't update the funding criteria")
    @api.response(HTTPStatus.NOT_FOUND, "Investor  specified doesn't exist")
    def patch(self, funding_criteria_id):
        """Update a Funding criteria."""
        funding_criteria = get_funding_criteria_by_id(funding_criteria_id)
        if not funding_criteria:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding criteria not found"
            )
        else:
            data = request.json
            return update_funding_criteria(data, funding_criteria)
