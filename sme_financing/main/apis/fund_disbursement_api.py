from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from ..service.fund_disbursement_service import (
    delete_disbursement,
    get_all_fund_disbursements,
    get_fund_disbursement_by_id,
    save_disbursement,
    update_fund_disbursement,
)
from .dto import FundDisbursementDTO

api = FundDisbursementDTO.fund_disbursement_api
_fund_disbursement = FundDisbursementDTO.fund_disburse


@api.route("/")
class fundDisbursementResource(Resource):
    @api.doc("List all funding disbursements")
    @api.marshal_list_with(_fund_disbursement, envelope="data")
    def get(self):
        """List all fund disbursements"""

        return get_all_fund_disbursements()

    @api.doc("Create a new fund disbursement")
    @api.expect(_fund_disbursement, validate=True)
    @api.response(201, "Funding disbursement successfully created")
    def post(self):
        """
        Create a new funding criteria
        """
        data = request.json
        return save_disbursement(data=data)


@api.route("/<int:fund_disbursement_id>")
@api.param("fund_disbursement_id", "The ID of the fund disbursement to process")
@api.response(HTTPStatus.NOT_FOUND, "Fund  disbursement not found")
class FundDisbursementById(Resource):
    @api.doc("Get a single fund disbursement")
    @api.marshal_with(_fund_disbursement)
    def get(self, fund_disbursement_id):
        """
        Retrieve funding disbursement for the given Id
        """
        fund_disburse = get_fund_disbursement_by_id(fund_disbursement_id)

        if not fund_disburse:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Fund disbursement not found"
            )
        else:
            return fund_disburse

    @api.doc("Delete fund disbursement")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete the fund disbursement")
    def delete(self, fund_disbursement_id):
        """
        Delete the fund disbursement  by the given Id to delete it
        """
        fund_disbursement = get_fund_disbursement_by_id(fund_disbursement_id)
        if not fund_disbursement:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding disbursement not found"
            )
        else:
            return delete_disbursement(fund_disbursement)

    @api.doc("Update a funding disbursement")
    @api.expect(_fund_disbursement, validate=True)
    @api.response(HTTPStatus.CREATED, "Fund disbursement successfully updated")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't update the fund disbursement")
    @api.response(HTTPStatus.NOT_FOUND, "funding_project  specified doesn't exist")
    def patch(self, fund_disbursement_id):
        """Update a Funding disbursement."""
        fund_disbursement = get_fund_disbursement_by_id(fund_disbursement_id)
        if not id:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Fund disbursement not found"
            )
        else:
            data = request.json
            return update_fund_disbursement(data, fund_disbursement)
