from sqlalchemy.exc import SQLAlchemyError

from .. import db
from ..models.funding_detail import FundingDetail
from ..service.document_service import get_all_funding_detail_documents, get_document
from ..service.funding_project_service import get_funding_project_by_id


def update():
    db.commit()


def commit_changes(new_data):

    db.session.add(new_data)
    update()


def save_funding_detail(data):
    """This method saves new funding details data"""
    funding_project = get_funding_project_by_id(id=data["funding_project_id"])

    if not funding_project:
        fund_detail = FundingDetail(name=data["name"], description=data["description"])
        fund_detail.funding_project_id = funding_project

        try:
            commit_changes(fund_detail)
            response_object = {
                "status": "success",
                "message": "Fund details added successfully",
            }
            return response_object, 201
        except SQLAlchemyError as error:
            response_object = {"status": "failure", "message": str(error)}

    else:
        response_object = {
            "status": "failure",
            "message": "funding detail already exist",
        }
        return response_object, 504


def update_fund_detail(data, fund_detail):
    """This method updates the information stored in a fund detail."""
    if data.get("name"):
        fund_detail.name = data["name"]
    if data.get("description"):
        fund_detail.name = data["description"]

    funding_project = get_funding_project_by_id(id=data["funding_project_id"])
    if funding_project:
        fund_detail.funding_project_id = funding_project
        try:
            update()
            response_object = {"status": "success", "message": "Successfully updated. "}
            return response_object, 202
        except SQLAlchemyError as error:
            db.session.rollback()
            response_object = {"status": "failure", "message": str(error)}
            return response_object, 400
    else:
        response_object = {
            "status": "failure",
            "message": "Invalid  funding project",
        }
        return response_object, 404


def delete_fund_detail(fund_detail):
    try:
        db.session.delete(fund_detail)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "Fund detail successfully deleted",
        }
        return response_object, 204
    except SQLAlchemyError as error:
        db.session.rollback()
        response_object = {"status": "failure", "message": str(error)}
        return response_object, 500


def get_fund_detail_by_id(fund_detail_id):
    return FundingDetail.query.filter_by(id=fund_detail_id).first()


def get_all_fund_detail():
    return FundingDetail.query.all()
