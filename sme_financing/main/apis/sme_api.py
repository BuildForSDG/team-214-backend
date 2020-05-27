"""RESTful API SME resource."""

from flask import request
from flask_restx import Resource
from flask_restx._http import HTTPStatus

from ..service.sme_service import delete_sme, get_all_smes, get_sme_by_id, save_sme
from .dto import SMEDTO, DocumentDTO

api = SMEDTO.sme_api
_sme = SMEDTO.sme
_sme_list = SMEDTO.sme_list
_document = DocumentDTO.document


@api.route("/")
class SMEList(Resource):
    @api.doc("list of SMEs")
    @api.marshal_list_with(_sme_list, envelope="data")
    def get(self):
        """List all SMEs."""
        return get_all_smes()

    @api.doc("Register a new SME")
    @api.expect(_sme, validate=True)
    @api.response(201, "SME successfully registered")
    def post(self):
        """Register a new SME."""
        data = request.json
        return save_sme(data=data)


@api.route("/<int:sme_id>")
@api.param("sme_id", "The ID of the SME to process")
@api.response(HTTPStatus.NOT_FOUND, "SME not found")
class SMEByID(Resource):
    @api.doc("Get a single SME")
    @api.marshal_with(_sme)
    def get(self, sme_id):
        """Retrieve an SME."""
        sme = get_sme_by_id(sme_id)
        if not sme:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="SME not found")
        else:
            return sme

    @api.doc("Delete an SME")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete SME")
    def delete(self, sme_id):
        """Delete an SME."""
        sme = get_sme_by_id(sme_id)
        if not sme:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="SME not found")
        else:
            return delete_sme(sme)


@api.route("/<int:sme_id>/documents")
@api.param("sme_id", "The SME id")
@api.response(HTTPStatus.NOT_FOUND, "SME not found")
class SMEDocuments(Resource):
    @api.doc("List all documents of an SME")
    @api.marshal_list_with(_document, envelope="data")
    def get(self, sme_id):
        """List all documents of an SME."""
        sme = get_sme_by_id(sme_id)
        if not sme:
            self.api.abort(HTTPStatus.NOT_FOUND, message="SME not found")
        else:
            return sme.documents
