import json
import os

import firebase_admin
import requests
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

firebase = firebase_admin.initialize_app()

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


def login_with_email_and_password(data, return_secure_token: bool = True):
    user_email = data["email"]
    user_password = data["password"]
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
            response_object = {"status": "failure", "message": "Invalid token"}
            return response_object, 502
    else:
        pass


if __name__ == "__main__":
    data = {"email": "akoladenis97@gmail.com", "password": "buildforsdg"}
    data_v = login_with_email_and_password(data=data)
    print(data_v)
    # print("--------------")
    # print(verify_user(data_v))
    # #print(login_with_email_and_password(data=data))
