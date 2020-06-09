from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from ..service.funding_detail_service import (
    delete_fund_detail,
    get_all_fund_detail,
    get_fund_detail_by_id,
    save_funding_detail,
    update_fund_detail,
)
from .dto import FundDetailDTO

api = FundDetailDTO.fund_detail_api
_fund_detail = FundDetailDTO.fund_detail_api


@api.route("/funding_detail")
class fundDetailResource(Resource):
    @api.doc("List all funding details")
    @api.marshal_list_with(_fund_detail, envelope="data")
    def get(self):
        """
        List all funding criteria
        """
        return get_all_fund_detail()

    @api.doc("Create a new fund detail")
    @api.expect(_fund_detail, validate=True)
    @api.response(201, "Funding detail successfully created")
    def post(self):
        """
        Create a new funding criteria
        """
        data = request.json
        return save_funding_detail(data=data)


@api.route("/fund_detail/<int:fund_detail_id>")
@api.param("fund_detail_id", "The ID of the Funding detail to process")
@api.response(HTTPStatus.NOT_FOUND, "Fund detail  not found")
class FundDetailById(Resource):
    @api.doc("Get a single fund detail")
    @api.marshal_with(_fund_detail)
    def get(self, fund_detail_id):
        """
        Retrieve funding detail for the given Id
        """
        fund_detail = get_all_fund_detail(fund_detail_id)

        if not fund_detail:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="Fund detail  not found")
        else:
            return fund_detail

    @api.doc("Delete fund detail")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete the fund detail")
    def delete(self, fund_detail_id):
        """
        Delete the fund detail by the given Id to delete it
        """
        fund_detail = get_fund_detail_by_id(id=fund_detail_id)
        if not fund_detail:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="Fund detail not found")
        else:
            return delete_fund_detail(fund_detail)

    @api.doc("Update a fund detail")
    @api.expect(_fund_detail, validate=True)
    @api.response(HTTPStatus.CREATED, "Funding detail successfully updated")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't update the funding detail")
    @api.response(HTTPStatus.NOT_FOUND, "Funding project  specified doesn't exist")
    def patch(self, fund_detail_id):
        """Update a fund detail"""
        fund_detail = get_fund_detail_by_id(id=fund_detail_id)
        if not fund_detail_id:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="Fund detail not found")
        else:
            data = request.json
            return update_fund_detail(data, fund_detail)
