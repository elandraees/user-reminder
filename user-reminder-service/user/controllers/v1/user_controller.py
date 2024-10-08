from flask import Blueprint, make_response
from util import json_util
from util.controller_helper import *

user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('/create', methods=['POST'])
@authenticate_secret
def create_user():
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)

    try:
        account: User = account_service.create_user(json)
        return api_response.get_success_response("Successfully created account", account.to_json())
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@user_bp.route('/list', methods=['GET'])
@authenticate_secret
def get_accounts():
    try:
        accounts: [dict] = account_service.get_user_list()
        return api_response.get_success_response("", accounts)
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@user_bp.route('/authenticate', methods=['GET'])
@authenticate_user_password
def get_user_auth_token():
    try:
        token_dict = account_service.get_auth_token(get_username())
        response = make_response(api_response.get_success_response("", token_dict))
        response.set_cookie('access_token_cookie', token_dict['token'], httponly=True, secure=True, samesite='None')
        return response
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@user_bp.route('/logout', methods=['GET'])
@authenticate_token
def logout():
    try:
        response = make_response(api_response.get_success_response("", ""))
        response.set_cookie('access_token_cookie', '', expires=0, httponly=True, secure=True, samesite='None')
        return response
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@user_bp.route('/has_auth', methods=['GET'])
@authenticate_token
def has_auth_token():
    try:
        return api_response.get_success_response("", "")
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@user_bp.route('/', methods=['GET'])
@authenticate_token
def get_account():
    try:
        account: User = account_service.get_user(get_username())
        return api_response.get_success_response("", account.to_json_include_id())
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@user_bp.route('/update', methods=['POST'])
@authenticate_token
def update_account():
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)

    try:
        account_data: User = account_service.update_user(json, get_username())
        return api_response.get_success_response("Successfully updated account", account_data.to_json())
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)
