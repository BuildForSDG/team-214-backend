from sqlalchemy.exc import SQLAlchemyError

from .. import db
from ..models.funding_criteria import FundingCriteria
from .investor_service import get_investor_by_id


def update():
    db.commit()


def commit_changes(new_data):
    """
    This method commits new changes to the funding_criteria model
    """
    db.session.add(new_data)
    update()


def save_funding_criteria(data):
    """
    This method saves the new funding criteria data
    """

    investor = get_investor_by_id(data["investor_id"])
    if not investor:
        fund_criteria = FundingCriteria(
            title=data["title"],
            description=data["description"],
            investor_id=data["investor_id"],
        )

        fund_criteria.investor = investor

        try:
            commit_changes(fund_criteria)
            response_object = {
                "status": "success",
                "message": "Funding criteria successfully added!",
            }
            return response_object, 201
        except SQLAlchemyError as error:
            response_object = {"status": "failure", "message": str(error)}
            return response_object, 500
    else:
        response_object = {"status": "failure", "message": "Invalid investor id"}
        return response_object, 500


def update_funding_criteria(data, funding_criteria):
    """
    This method updates the funding criteria data in the database

    """
    # checking for the updated field

    if data.get("title"):
        funding_criteria.title = data["title"]
    if data.get("description"):
        funding_criteria.description = data["description"]

    investor = get_investor_by_id(id=data["investor_id"])
    if not investor:
        response_object = {
            "status": "failure",
            "message": "Invalid Investor id!.",
        }
        return response_object, 404
    else:
        funding_criteria.investor = investor
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


def delete_funding_criteria(funding_criteria):
    try:
        db.session.delete(funding_criteria)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "Funding criteria successfully deleted!",
        }
        return response_object, 204
    except SQLAlchemyError as error:
        db.session.rollback()
        response_object = {"status": "error", "message": str(error)}
        return response_object, 500


def get_funding_criteria_by_id(funding_criteria_id):

    return FundingCriteria.query.filter_by(id=funding_criteria_id).first()


def get_all_funding_criteria():
    return FundingCriteria.query.all()
