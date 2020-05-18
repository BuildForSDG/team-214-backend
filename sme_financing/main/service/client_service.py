import uuid

from .. import db
from ..models.client import Client
from ..models.user import User


def commit_changes(data):
    db.session.add(data)
    db.session.commit()


def save_client(data):
    user = User.query.filter_by(email=data["user"]["email"]).first()
    if not user:
        new_user = User(
            email=data["user"]["email"],
            username=data["user"]["username"],
            password=data["user"]["password"],
            public_id=data["user"]["public_id"] or str(uuid.uuid4()),
            # registered_on=datetime.datetime.utcnow()
        )
        new_client = Client(
            lastname=data["lastname"],
            firstname=data["firstname"],
            gender=data["gender"],
            postal_address=data["postal_address"],
            residential_address=data["residential_address"],
            telephone=data["telephone"],
            nationality=data["nationality"],
            education_level=data["education_level"],
            position=data["position"],
        )
        new_client.user = new_user
        commit_changes(new_client)
        response_object = {"status": "success", "message": "Successfully registered."}
        return response_object, 201  # success & resource created
    else:
        response_object = {
            "status": "fail",
            "message": "Client/User already exists. Please Log in.",
        }
        return response_object, 409  # conflict with current state


def get_all_clients():
    return Client.query.all()


def get_client_by_user_id(user_id):
    return Client.query_filter_by(user_id=user_id).first()


def get_client_by_email(email):
    return Client.query.filter(Client.user.has(email=email)).first()

# def get_client_by_email(email):
#     return Client.query.join(Client.user, aliased=True).filter_by(email=email).first()
