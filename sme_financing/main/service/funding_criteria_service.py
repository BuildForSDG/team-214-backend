from sqlalchemy.exc import SQLAlchemyError

from .. import db
from ..models.funding_criteria import FundingCriteria
from .investor_service import get_investor_by_id


def commit_changes(new_data):
    """
    This method commits new changes to the funding_criteria model


    """
    db.session.add(new_data)
    db.session.commit()


def save_funding_criteria(data):
    """
    This method saves the new funding criteria data
    """
    fund_criteria = FundingCriteria(
        name=data["name"],
        description=data["description"],
        investor_id=data["investor_id"],
    )
    Investor = get_investor_by_id(data["investor_id"])
    if not Investor:
        response_object = {
            "status": "error",
            "message": "Invalid investor!",
        }
        return response_object, 409
    else:
        fund_criteria.investor_id = Investor
        try:
            commit_changes(fund_criteria)
            response_object = {
                "status": "success",
                "message": "Fund criteria successfully added!",
            }
            return response_object, 201
        except SQLAlchemyError as error:
            response_object = {"status": "error", "message": str(error)}
            return response_object, 500


def update_funding_criteria(data, funding_criteria):
    """
    This method updates the funding criteria data in the database

    """
    # checking for the updated field
    if data.get("name"):
        funding_criteria.name = data["name"]
    if data.get("description"):
        funding_criteria.description = data["description"]
    if data.get("investor_id"):
        funding_criteria.investor_id = data["investor_id"]

    # Checking  for a valid investor using the investor id
    Investor = get_investor_by_id(data["investor_id"])
    if not Investor:
        response_object = {
            "status": "fail",
            "message": "Invalid Investor id!.",
        }
        return response_object, 404
    else:
        try:
            db.session.add(funding_criteria)
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Successfully updated!",
            }
            return response_object, 201

        except SQLAlchemyError as error:
            response_object = {"status": "error", "message": str(error)}
            return response_object, 400


def delete_funding_criteria(funding_criteria):
    try:
        db.session.delete(funding_criteria)
        db.commit()
        response_object = {
            "status": "success",
            "message": "Funding Application successfully deleted!",
        }
        return response_object, 204
    except SQLAlchemyError as error:
        response_object = {"status": "error", "message": str(error)}
        return response_object, 500


def get_funding_criteria_by_id(funding_criteria_id):
    return FundingCriteria.query.filter_by(id=funding_criteria_id)


def get_all_funding_criteria():
    return FundingCriteria.query.all()
