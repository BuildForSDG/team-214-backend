"""RESTful Investor resource."""

from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from ..service.investor_service import (
    delete_investor,
    get_all_investors,
    get_investor_by_id,
    save_investor,
    update_investor,
)
from .dto import InvestorDTO

api = InvestorDTO.investor_api
_investor = InvestorDTO.investor


@api.route("/")
class InvestorList(Resource):
    @api.doc("list of Investors")
    @api.marshal_list_with(_investor, envelope="data")
    def get(self):
        """List all Investors."""
        return get_all_investors()

    @api.doc("Register a new Investor")
    @api.expect(_investor, validate=True)
    @api.response(201, "Investor successfully registered")
    def post(self):
        """Register a new Investor."""
        data = request.json
        return save_investor(data=data)


@api.route("/<int:investor_id>")
@api.param("investor_id", "The ID of the Investor to process")
@api.response(HTTPStatus.NOT_FOUND, "Investor not found")
class InvestorByID(Resource):
    @api.doc("Get a single Investor")
    @api.marshal_with(_investor)
    def get(self, investor_id):
        """Retrieve an Investor by ID."""
        investor = get_investor_by_id(investor_id)
        if not investor:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="Investor not found")
        else:
            return investor

    @api.doc("Delete an Investor")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete the Investor")
    def delete(self, investor_id):
        """Delete an Investor."""
        investor = get_investor_by_id(investor_id)
        if not investor:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="Investor not found")
        else:
            return delete_investor(investor)

    @api.doc("Update a Investor")
    @api.expect(_investor, validate=True)
    @api.response(HTTPStatus.CREATED, "Investor successfully updated")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't update the Investor")
    def patch(self, investor_id):
        """Update an Investor."""
        investor = get_investor_by_id(investor_id)
        if not investor:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="Investor not found")
        else:
            data = request.json
            return update_investor(data, investor)
