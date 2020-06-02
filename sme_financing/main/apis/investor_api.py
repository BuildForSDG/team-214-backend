"""RESTful Investor resource."""

from flask import request
from flask_restx import Resource

from ..service.investor_service import get_all_investors, save_investor
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
