import json
import os

import requests
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")

rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


def login_with_email_and_password(data, return_secure_token: bool = True):

    payload = json.dumps(
        {
            "email": data["email"],
            "password": data["password"],
            "returnSecureToken": return_secure_token,
        }
    )
    r = requests.post(rest_api_url, params={"key": FIREBASE_WEB_API_KEY}, data=payload)
    return r.json()


def verify_user(token):
    """
    Verifies the signature and data for the provided JWT.
    Accepts a signed token string, verifies that it is current, and issued to this project,
    and that it was correctly signed by Google
    """
    if len(token) > 1:
        # if a token is generated,the length of the token dict will be greater than 1

        try:
            auth.verify_id_token(token["idToken"])
            response_object = {
                "status": "success",
                "message": "Successfully registered.",
            }
            return response_object, 202
        except FirebaseError as error:
            response_object = {"status": "failure", "message": str(error)}
            return response_object, 502
    else:
        pass


def forget_password(email: str):
    """
    It takes an email and sent a reset password email to the user

    """
    user = auth.get_user_by_email(email=email)
    if user:

        try:
            auth.generate_password_reset_link(email=email)
            response_object = {
                "status": "success",
                "message": "Link sent!",
            }
            return response_object, 202
        except FirebaseError as error:
            response_object = {"status": "failed", "message": str(error)}
            return response_object, 502
    response_object = {"status": "failed", "message": "Email does not exist!"}
    return response_object, 500


def reset_password(id, data):
    new_password = data["password"]
    confirm_password = data["confirmpassword"]
    if new_password == confirm_password:
        try:
            auth.updata_user(id, password=new_password)
            response_object = {
                "status": "success",
                "message": "password reset successful",
            }
            return response_object, 202
        except FirebaseError as error:
            response_object = {"status": "failure", "message": str(error)}
    response_object = {"status": "failure", "message": "Inconsistent password"}
    return response_object, 503
