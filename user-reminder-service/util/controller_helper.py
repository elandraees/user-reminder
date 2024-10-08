import util.encryption_util as encryption_util
import util.jwt_util as jwt_util
import util.constants as constants
from base64 import b64decode
import util.validation_util as validation_util
from functools import wraps
import util.api_response as api_response
from flask import request
import datetime
import user.services.user_service as account_service
from user.models.user import User
from datetime import datetime


account_api_key = ""
username = ""
password = ""
user_id = 0


def authenticate_secret(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        service_key = request.headers.get(constants.SECRET_KEY_HEADER)
        if validation_util.is_none_empty_or_zero(service_key) or service_key != constants.SECRET_KEY:
            return api_response.get_error_response("Insufficient Authorization", "", 401)

        return fn(*args, **kwargs)

    return wrapper


def authenticate_user_password(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global username
        global password
        global user_id
        header = request.headers.get(constants.AUTH_HEADER)
        if header is None or not header.startswith(constants.BASIC_AUTH_HEADER):
            return api_response.get_error_response("Insufficient Authorization", "", 401)
        token = header[6:]
        username, password = b64decode(token).decode().split(':', 1)
        if not username or not password:
            return api_response.get_error_response("No Username or Password Specified", "", 401)

        account: User = account_service.get_user(username)
        if not encryption_util.check_hash(password, account.password):
            return api_response.get_error_response("Password or Username is incorrect", "", 401)
        user_id = account.user_id

        return fn(*args, **kwargs)

    return wrapper


def authenticate_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global username
        global user_id
        jwt_decoded_token = jwt_util.get_decoded_token(request)
        if jwt_decoded_token is None:
            return api_response.get_error_response("Insufficient Authorization", "", 401)
        exp = jwt_decoded_token.get(constants.JWT_PAYLOAD_EXP)
        if exp < int(datetime.utcnow().timestamp()):
            return api_response.get_error_response("Insufficient Authorization", "", 401)
        user_id = jwt_decoded_token.get(constants.JWT_PAYLOAD_USER_ID)
        username = jwt_decoded_token.get(constants.JWT_PAYLOAD_USERNAME)
        if username is None or user_id is None:
            return api_response.get_error_response("Insufficient Authorization", "", 401)
        return fn(*args, **kwargs)

    return wrapper


def __decode_token() -> str | None:
    global username
    global user_id
    jwt_decoded_token = jwt_util.get_decoded_token(request)
    if jwt_decoded_token is None:
        return api_response.get_error_response("Insufficient Authorization", "", 401)
    exp = jwt_decoded_token.get(constants.JWT_PAYLOAD_EXP)
    if exp < int(datetime.utcnow().timestamp()):
        return api_response.get_error_response("Insufficient Authorization", "", 401)
    user_id = jwt_decoded_token.get(constants.JWT_PAYLOAD_USER_ID)
    username = jwt_decoded_token.get(constants.JWT_PAYLOAD_USERNAME)
    if username is None or user_id is None:
        return api_response.get_error_response("Insufficient Authorization", "", 401)


def get_username():
    return username


def get_user_id():
    return user_id
