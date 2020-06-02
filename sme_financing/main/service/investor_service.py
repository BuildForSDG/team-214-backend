from sqlalchemy.exc import SQLAlchemyError

from .. import db
from ..models.investor import Investor


def update():
    db.session.commit()


def commit_changes(data):
    db.session.add(data)
    update()


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


def delete_investor(investor):
    try:
        db.session.delete(investor)
        update()
        response_object = {
            "status": "success",
            "message": "Investor successfully deleted.",
        }
        return response_object, 204
    except SQLAlchemyError as e:
        db.session.rollback()
        response_object = {"status": "error", "message": str(e)}
        return response_object, 400


def update_investor(data, investor):
    if data.get("name"):
        investor.name = data["name"]
    if data.get("postal_address"):
        investor.postal_address = data["postal_address"]
    if data.get("street_address"):
        investor.street_address = data["street_address"]
    if data.get("city"):
        investor.city = data["city"]
    if data.get("telephone"):
        investor.telephone = data["telephone"]
    if data.get("email"):
        investor.email = data["email"]
    if data.get("investor_type"):
        investor.investor_type = data["investor_type"]

    try:
        update()
        response_object = {
            "status": "success",
            "message": "Investor successfully updated.",
        }
        return response_object, 201
    except SQLAlchemyError as err:
        db.session.rollback()
        response_object = {"status": "error", "message": str(err)}
        return response_object, 400


def get_all_investors():
    return Investor.query.all()


def get_investor_by_id(investor_id):
    return Investor.query.filter_by(id=investor_id).first()
