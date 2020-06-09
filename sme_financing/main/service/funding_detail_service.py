from sqlalchemy.exc import SQLAlchemyError

from sme_financing.main import db

from ..models.funding_detail import FundingDetail
from ..service.document_service import create_document_instance


def update():
    db.session.commit()


def commit_changes(data):
    db.session.add(data)
    update()


def create_funding_detail(data, funding_project):
    funding_detail = FundingDetail(title=data["title"], description=data["description"])
    document = create_document_instance(data["document_name"], data["file"])
    funding_detail.add_document(document)
    funding_project.add_funding_detail(funding_detail)

    try:
        funding_project.update()
        response_object = {
            "status": "success",
            "message": "Funding detail successfully added.",
        }
        return response_object, 201
    except SQLAlchemyError as error:
        response_object = {"status": "error", "message": str(error)}
        return response_object, 400


def add_document(data, funding_detail):
    document = create_document_instance(data["document_name"], data["file"])
    funding_detail.add_document(document)
    try:
        funding_detail.update()
        response_object = {
            "status": "success",
            "message": "Document successfully added.",
        }
        return response_object, 201
    except SQLAlchemyError as error:
        response_object = {"status": "error", "message": str(error)}
        return response_object, 400


def update_funding_detail(data, funding_detail):
    if data.get("title"):
        funding_detail.title = data["title"]
    if data.get("description"):
        funding_detail.description = data["description"]

    try:
        update()
        response_object = {
            "status": "success",
            "message": "Successfully updated.",
        }
        return response_object, 201
    except SQLAlchemyError as err:
        db.session.rollback()
        response_object = {"status": "error", "message": str(err)}
        return response_object, 400


def delete_funding_detail(funding_detail):
    try:
        db.session.delete(funding_detail)
        update()
        response_object = {
            "status": "success",
            "message": "Funding detail successfully deleted.",
        }
        return response_object, 204
    except SQLAlchemyError as e:
        db.session.rollback()
        response_object = {"status": "error", "message": str(e)}
        return response_object, 400


def get_all_funding_details():
    return FundingDetail.query.all()


def get_funding_detail_by_id(funding_detail_id):
    return FundingDetail.query.filter_by(id=funding_detail_id).first()


def get_project_funding_details(funding_project_id):
    return FundingDetail.query.filter_by(funding_project_id=funding_project_id)
