from sqlalchemy.exc import SQLAlchemyError

from .. import db
from ..models.funding_application import FundingApplication
from .sme_service import get_sme_by_email


def update():
    db.session.commit()


def commit_changes(data):
    db.session.add(data)
    update()


def save_funding_application(data):
    new_funding_application = FundingApplication(
        number=data["number"], status=data["status"]
    )
    sme = get_sme_by_email(data["sme_email"])
    if not sme:
        response_object = {
            "status": "error",
            "message": "SME specified doesn't exist.",
        }
        return response_object, 409

    else:
        new_funding_application.sme = sme
        try:
            commit_changes(new_funding_application)
            response_object = {
                "status": "success",
                "message": "Successfully created.",
            }
            return response_object, 201
        except SQLAlchemyError as error:
            response_object = {"status": "error", "message": str(error)}
            return response_object, 500


def update_funding_application(data, funding_application):
    if data.get("number"):
        funding_application.number = data["number"]
    if data.get("status"):
        funding_application.status = data["status"]
    if data.get("sme_email"):
        sme = get_sme_by_email(data["sme_email"])
        if not sme:
            response_object = {
                "status": "error",
                "message": "SME specified doesn't exist.",
            }
            return response_object, 404
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


def delete_funding_application(funding_application):
    try:
        db.session.delete(funding_application)
        update()
        response_object = {
            "status": "success",
            "message": "Funding Application successfully deleted.",
        }
        return response_object, 204
    except SQLAlchemyError as e:
        db.session.rollback()
        response_object = {"status": "error", "message": str(e)}
        return response_object, 500


def get_funding_application_by_id(funding_application_id):
    return FundingApplication.query.filter_by(id=funding_application_id).first()


def get_funding_application_by_number(number):
    return FundingApplication.query.filter_by(number=number).first()


def get_all_funding_applications():
    return FundingApplication.query.all()


def register_investor_interest(funding_application, investor, investor_message):
    if investor in funding_application.investors:
        response_object = {
            "status": "fail",
            "message": "This investor is already interested",
        }
        return response_object, 400
    # funding_application.investors.append(investor)
    funding_application.add_investor(investor, investor_message)
    try:
        update()
        response_object = {
            "status": "success",
            "message": "Successfully registered.",
        }
        return response_object, 201
    except SQLAlchemyError as err:
        db.session.rollback()
        response_object = {"status": "error", "message": str(err)}
        return response_object, 500


def get_interested_investors(funding_application_id):
    funding_application = get_funding_application_by_id(funding_application_id)
    if not funding_application:
        response_object = {
            "status": "error",
            "message": "Funding Application specified doesn't exist.",
        }
        return response_object, 404
    else:
        return funding_application.investors


def remove_interested_investor(funding_application, investor):
    if investor not in funding_application.investors:
        response_object = {
            "status": "fail",
            "message": """Investor hasn't registered interest""",
        }
        return response_object, 400
    funding_application.investors.remove(investor)
    try:
        update()
        response_object = {
            "status": "success",
            "message": "Successfully removed.",
        }
        return response_object, 201
    except SQLAlchemyError as err:
        db.session.rollback()
        response_object = {"status": "error", "message": str(err)}
        return response_object, 500
