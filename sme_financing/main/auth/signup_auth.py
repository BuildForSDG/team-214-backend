from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

def sign_up_with_email_and_password(email: str, password: str):
    # Retrieve the signup details from a dictionary
    user_email = email
    user_password = password
    # user = auth.get_user_by_email(email=email)
    try:
        auth.create_user(email=user_email, password=user_password)
        response_object = {"status": "success", "message": "Successfully registered."}
        return response_object, 201  # success & resource created
    except FirebaseError as error:
        response_object = {"status": "error", "message": str(error)}
        return response_object, 500


if __name__ == "__main__":
    print(sign_up_with_email_and_password("akoladenis97@gmail.com", "buildforsdg"))
