from sqlalchemy.exc import SQLAlchemyError

from .. import db
from ..models.investor import Investor


def commit_changes(data):
    db.session.add(data)
    db.session.commit()


def save_investor(data):
    new_investor = Investor(
        name=data["name"],
        postal_address=data["postal_address"],
        street_address=data["street_address"],
        city=data["city"],
        telephone=data["telephone"],
        email=data["email"],
        investor_type=data["investor_type"],
    )
    try:
        commit_changes(new_investor)
        response_object = {"status": "success", "message": "Successfully registered."}
        return response_object, 201  # success & resource created
    except SQLAlchemyError as error:
        response_object = {"status": "error", "message": str(error)}
        return response_object, 500


def get_all_investors():
    return Investor.query.all()


def get_investor_by_id(investor_id):
    return Investor.query.filter_by(id=investor_id).first()
