from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from .. import db
from ..models.sme import SME
from .client_service import get_client_by_email

# from .document_service import get_all_sme_documents


def commit_changes(data):
    db.session.add(data)
    db.session.commit()


def save_sme(data):
    new_sme = SME(
        name=data["name"],
        postal_address=data["postal_address"],
        location=data["location"],
        telephone=data["telephone"],
        email=data["email"],
        description=data["description"],
        sector=data["sector"],
        principal_product_service=data["principal_product_service"],
        other_product_service=data["other_product_service"],
        age=data["age"],
        establishment_date=datetime.strptime(
            data["establishment_date"], "%Y-%m-%d"
        ).date(),
        ownership_type=data["ownership_type"],
        bank_account_details=data["bank_account_details"],
        employees_number=data["employees_number"],
    )
    client = get_client_by_email(data["client_email"])

    if not client:
        response_object = {
            "status": "fail",
            "message": "Client/User doesn't exists.",
        }
        return response_object, 409

    else:
        new_sme.client = client
        try:
            commit_changes(new_sme)
            response_object = {
                "status": "success",
                "message": "Successfully registered.",
            }
            return response_object, 201
        except SQLAlchemyError as error:
            response_object = {"status": "error", "message": str(error)}
            return response_object, 500


def delete_sme(sme):
    # sme.delete()
    try:
        db.session.delete(sme)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "SME successfully deleted.",
        }
        return response_object, 204
    except SQLAlchemyError as e:
        db.session.rollback()
        response_object = {"status": "error", "message": str(e)}
        return response_object, 400


def get_all_smes():
    return SME.query.all()


def get_sme_by_id(id):
    return SME.query.filter_by(id=id).first()


def get_all_sme_documents(id):
    return get_sme_by_id(id).documents
