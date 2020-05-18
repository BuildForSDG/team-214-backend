import uuid

from .. import db
from ..models.user import User


def commit_changes(data):
    db.session.add(data)
    db.session.commit()


def save_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            public_id=data['public_id'] or str(uuid.uuid4()),
            # registered_on=datetime.datetime.utcnow()
        )
        commit_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201  # success & resource created
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409  # conflict with current state


def get_all_users():
    return User.query.all()


def get_user_by_public_id(public_id):
    return User.query.filter_by(public_id=public_id).first()
