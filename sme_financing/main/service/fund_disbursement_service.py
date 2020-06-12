from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from sme_financing.main import db

from ..models.fund_disbursement import FundDisbursement
from ..service.funding_project_service import get_funding_project_by_id


def update():
    db.session.commit()


def commit_changes(data):
    db.session.add(data)
    update()


def save_disbursement(data):
    funding_project = get_funding_project_by_id(id=data["funding_project_id"])
    if funding_project:
        new_disburse = FundDisbursement(
            description=data["description"],
            status=data["status"],
            disbursement_date=datetime.strptime(
                data["disbursement_date"], "%Y-%m-%d"
            ).date(),
            bank_account_details_from=data["bank_account_details_from"],
            bank_account_details_to=data["bank_account_details_to"],
            cheque_details=data["cheque_details"],
        )
        new_disburse.funding_project_id = funding_project

        try:
            commit_changes(new_disburse)
            response_object = {
                "status": "success",
                "message": "Funding disbursement successfully added!",
            }
            return response_object, 201
        except SQLAlchemyError as error:
            response_object = {
                "status": "failure",
                "message": str(error),
            }
            return response_object, 500
    else:
        response_object = {
            "status": "failure",
            "message": " Invalid funding project id!",
        }
        return response_object, 500


def update_fund_disbursement(data, disbursement_data):

    if data.get("description"):
        disbursement_data.description = data["description"]

    if data.get("status"):
        disbursement_data.status = data["status"]

    if data.get("bank_account_details_from"):
        disbursement_data.bank_account_details_from = data["bank_account_details_from"]

    if data.get("bank_account_details_to"):
        disbursement_data.bank_account_details_to = data["bank_account_details_to"]

    funding_project = get_funding_project_by_id(id=data["funding_project_id"])

    if not funding_project:
        response_object = {"status": "failure", "message": "Update  was not successful"}
        return response_object, 404

    else:
        try:
            update()
            response_object = {"status": "success", "message": "Successfully updated."}
            return response_object, 201
        except SQLAlchemyError as err:
            db.session.rollback()
            response_object = {"status": "error", "message": str(err)}
            return response_object, 400


def delete_disbursement(fund_disbursement):
    try:
        db.session.delete(fund_disbursement)
        update()
        response_object = {
            "status": "success",
            "message": "Funding disbursement successfully deleted.",
        }
        return response_object, 204
    except SQLAlchemyError as e:
        db.session.rollback()
        response_object = {"status": "error", "message": str(e)}
        return response_object, 500


def get_fund_disbursement_by_id(fund_disbursement_id):
    return FundDisbursement.query.filter_by(id=fund_disbursement_id).first()


def get_all_fund_disbursements():
    return FundDisbursement.query.all()
