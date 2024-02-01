from functools import wraps
from flask import request, abort
from flask import current_app
from src.auth.auth_cognito import CognitoAuthenticator

pool_id = 'us-east-2_3xYKhXC3M'
pool_region = 'us-east-2'
client_id = '589v74d5ip29jcf899p7j18ct6'

auth = CognitoAuthenticator(
    pool_region=pool_region,
    pool_id=pool_id,
    client_id=client_id,
)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            token_verified = auth.verify_token(token)
            if token_verified is False:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated