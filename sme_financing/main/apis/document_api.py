"""RESTful API Document resource."""

from flask_restx import Resource, reqparse
from flask_restx._http import HTTPStatus
from werkzeug.datastructures import FileStorage

from ..service.document_service import (
    delete_document,
    edit_document,
    get_all_documents,
    get_document,
    save_document,
)
from .dto import DocumentDTO

api = DocumentDTO.document_api
_document = DocumentDTO.document

parser = reqparse.RequestParser()
parser.add_argument("document_name", type=str, help="Document name", location="form")
parser.add_argument("file", type=FileStorage, location="files")


@api.route("/")
class DocumentList(Resource):
    @api.doc("list of documents")
    @api.marshal_list_with(_document, envelope="data")
    def get(self):
        """List all documents."""
        return get_all_documents()

    @api.doc("Create a new Document")
    @api.expect(parser, validate=True)
    @api.response(HTTPStatus.CREATED, "Document successfully saved")
    @api.response(HTTPStatus.NOT_FOUND, "File not found")
    @api.response(HTTPStatus.BAD_REQUEST, "File empty")
    @api.response(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "File exceeds max upload size")
    @api.response(HTTPStatus.NOT_ACCEPTABLE, "File extension not allowed")
    def post(self):
        """Create a new Document."""
        parse_data = parser.parse_args()
        document_name = parse_data["document_name"]
        file = parse_data["file"]
        if not file or not document_name:
            self.api.abort(
                code=HTTPStatus.NOT_FOUND,
                message="File not found or document name empty",
            )
        else:
            return save_document(document_name, file)


@api.route("/<int:doc_id>")
@api.param("doc_id", "The ID of the docuemnt to process")
@api.response(HTTPStatus.NOT_FOUND, "Document not found")
@api.response(HTTPStatus.NOT_ACCEPTABLE, "File and document name empty")
class DocumentByID(Resource):
    @api.doc("Get a single document")
    @api.marshal_with(_document)
    def get(self, doc_id):
        """Retrieve a document."""
        document = get_document(doc_id)
        if not document:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="Document not found")
        else:
            return document

    @api.doc("Patch a document")
    @api.expect(parser)
    def patch(self, doc_id):
        """Patch a document."""
        document = get_document(doc_id)
        if not document:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="Document not found")
        else:
            parse_data = parser.parse_args()
            document_name = parse_data["document_name"]
            file = parse_data["file"]
            if not file and not document_name:
                self.api.abort(HTTPStatus.NOT_ACCEPTABLE, message="Both inputs empty")
            else:
                return edit_document(document, document_name, file)
                # return self.get(doc_id)

    @api.doc("Delete a document")
    @api.response(HTTPStatus.BAD_REQUEST, "Can't delete document")
    def delete(self, doc_id):
        """Delete a document."""
        document = get_document(doc_id)
        if not document:
            self.api.abort(code=HTTPStatus.NOT_FOUND, message="Document not found")
        else:
            return delete_document(document)


# @api.route("/smes/<sme_id>")
# @api.param("sme_id", "The SME id")
# @api.response(HTTPStatus.NOT_FOUND, "SME not found")
# class DocumentSME(Resource):
#     @api.doc("List all documents of an SME")
#     @api.marshal_list_with(_document, envelope="data")
#     def get(self, sme_id):
#         """List all documents of an SME."""
#         if not get_sme_by_id(sme_id):
#             api.abort(404)
#         return get_all_sme_documents(sme_id)
