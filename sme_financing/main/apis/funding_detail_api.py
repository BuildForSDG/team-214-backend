from flask import request
from flask_restx import Resource, reqparse
from flask_restx._http import HTTPStatus
from werkzeug.datastructures import FileStorage

from ..service import funding_detail_service as service
from .dto import FundingDetailDTO, DocumentDTO

api = FundingDetailDTO.funding_detail_api
_funding_detail = FundingDetailDTO.funding_detail
_document = DocumentDTO.document

_funding_detail_parser = reqparse.RequestParser()
_funding_detail_parser.add_argument(
    "document_name", required=True, type=str, help="Document name", location="form"
)
_funding_detail_parser.add_argument(
    "file", required=True, type=FileStorage, location="files"
)


@api.route("/")
class FundingDetail(Resource):
    @api.doc("list of funding details")
    @api.marshal_list_with(_funding_detail, envelope="data")
    def get(self):
        """List all funding details."""
        return service.get_all_funding_details()


@api.route("/<int:funding_detail_id>")
@api.param("funding_detail_id", "The ID of the funding detail to process")
@api.response(HTTPStatus.NOT_FOUND, "Funding detail not found")
class FundingDetailByID(Resource):
    @api.doc("Get a single funding detail")
    @api.marshal_with(_funding_detail)
    def get(self, funding_detail_id):
        """Retrieve an funding detail by ID."""
        funding_detail = service.get_funding_detail_by_id(funding_detail_id)
        if not funding_detail:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding detail not found"
            )
        else:
            return funding_detail

    @api.doc("Add a document to funding detail")
    @api.expect(_funding_detail_parser, validate=True)
    @api.response(HTTPStatus.NOT_FOUND, "Funding detail not found")
    @api.response(201, "Document successfully added")
    def post(self, funding_detail_id):
        """Add a document to funding detail."""
        funding_detail = service.get_funding_detail_by_id(funding_detail_id)
        if not funding_detail:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding detail not found"
            )
        else:
            data = _funding_detail_parser.parse_args()
            return service.add_document(data, funding_detail)

    @api.doc("Delete a funding detail")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete the funding detail")
    def delete(self, funding_detail_id):
        """Delete a funding detail."""
        funding_detail = service.get_funding_detail_by_id(funding_detail_id)
        if not funding_detail:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding detail not found"
            )
        else:
            return service.delete_funding_detail(funding_detail)

    @api.doc("Update a funding detail")
    @api.expect(_funding_detail, validate=True)
    @api.response(HTTPStatus.CREATED, "Funding detail successfully updated")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't update the funding detail")
    def patch(self, funding_detail_id):
        """Update a funding detail."""
        funding_detail = service.get_funding_detail_by_id(funding_detail_id)
        if not funding_detail:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding detail not found"
            )
        else:
            data = request.json
            return service.update_funding_detail(data, funding_detail)

@api.route("/<int:funding_detail_id>/documents")
@api.param("funding_detail_id", "The ID of the funding detail to process")
@api.response(HTTPStatus.NOT_FOUND, "Funding detail not found")
class FundingDetailDocument(Resource):
    @api.doc("Get a single funding detail")
    @api.marshal_with(_document)
    def get(self, funding_detail_id):
        """Retrieve an funding detail by ID."""
        funding_detail = service.get_funding_detail_by_id(funding_detail_id)
        if not funding_detail:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND, message="Funding detail not found"
            )
        else:
            return funding_detail.documents