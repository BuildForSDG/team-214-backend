from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from sme_financing.main import db

from ..models.funding_project import FundingProject
from .funding_application_service import get_funding_application_by_number
from .investor_service import get_investor_by_email


def update():
    db.session.commit()


def commit_changes(data):
    db.session.add(data)
    update()


def create_funding_project(data):
    fa_number = data["funding_application_number"]
    funding_application = get_funding_application_by_number(fa_number)
    if not funding_application:
        response_object = {
            "status": "error",
            "message": "Funding Application not found.",
        }
        return response_object, 404

    investor = get_investor_by_email(data["investor_email"])
    if not investor:
        response_object = {
            "status": "error",
            "message": "Investor not found.",
        }
        return response_object, 404

    funding_project = FundingProject(
        number=data["number"],
        title=data["title"],
        description=data["description"],
        relevance=data["relevance"],
        objectives=data["objectives"],
        justification=data["justification"],
        work_plan=data["work_plan"],
        status=data["status"],
        fund_amount=float(data["fund_amount"]),
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
        end_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
    )
    funding_project.funding_application = funding_application
    funding_project.investor = investor
    try:
        commit_changes(funding_project)
        response_object = {
            "status": "success",
            "message": "Project successfully created.",
        }
        return response_object, 201
    except SQLAlchemyError as error:
        response_object = {"status": "error", "message": str(error)}
        return response_object, 400


def delete_funding_project(funding_project):
    try:
        db.session.delete(funding_project)
        update()
        response_object = {
            "status": "success",
            "message": "Funding project successfully deleted.",
        }
        return response_object, 204
    except SQLAlchemyError as e:
        db.session.rollback()
        response_object = {"status": "error", "message": str(e)}
        return response_object, 400


def set_funding_project(data, funding_project):
    if data.get("title"):
        funding_project.title = data["title"]
    if data.get("description"):
        funding_project.description = data["description"]
    if data.get("relevance"):
        funding_project.relevance = data["relevance"]
    if data.get("objectives"):
        funding_project.objectives = data["objectives"]
    if data.get("justification"):
        funding_project.justification = data["justification"]
    if data.get("work_plan"):
        funding_project.work_plan = data["work_plan"]
    if data.get("status"):
        funding_project.status = data["status"]
    if data.get("fund_amount"):
        funding_project.fund_amount = float(data["fund_amount"])


def update_funding_project(data, funding_project):
    if data.get("investor_email"):
        investor = get_investor_by_email(data["investor_email"])
        if not investor:
            response_object = {
                "status": "error",
                "message": "Investor not found.",
            }
            return response_object, 404
    if data.get("funding_application_number"):
        fa_number = data["funding_application_number"]
        funding_application = get_funding_application_by_number(fa_number)
        if not funding_application:
            response_object = {
                "status": "error",
                "message": "Funding Application not found.",
            }
            return response_object, 404

    set_funding_project(data, funding_project)
    try:
        update()
        response_object = {
            "status": "success",
            "message": "Project successfully updated.",
        }
        return response_object, 201
    except SQLAlchemyError as err:
        db.session.rollback()
        response_object = {"status": "error", "message": str(err)}
        return response_object, 400


def get_all_funding_projects():
    return FundingProject.query.all()


def get_funding_project_by_number(number):
    return FundingProject.query.filter_by(number=number).first()


def get_funding_project_by_status(status):
    return FundingProject.query.filter_by(status=status)


def get_project_funding_details_by_number(number):
    funding_project = get_funding_project_by_number(number)
    if not funding_project:
        response_object = {
            "status": "error",
            "message": "Funding project not found.",
        }
        return response_object, 404
    else:
        return funding_project.funding_details


def get_project_project_milestones_by_number(number):
    funding_project = get_funding_project_by_number(number)
    if not funding_project:
        response_object = {
            "status": "error",
            "message": "Funding project not found.",
        }
        return response_object, 404
    else:
        return funding_project.project_milestones


def get_project_fund_disbursements_by_number(number):
    funding_project = get_funding_project_by_number(number)
    if not funding_project:
        response_object = {
            "status": "error",
            "message": "Funding project not found.",
        }
        return response_object, 404
    else:
        return funding_project.fund_disbursements


def get_funding_project_by_id(id):
    return FundingProject.query.filter_by(id=id).first()
