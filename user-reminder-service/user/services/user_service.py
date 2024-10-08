import util.json_util as json_util
import util.jwt_util as jwt_util
import user.repositories.user_repo as user_repo
import util.constants as constants
from user.models.user import User
import util.validation_util as validation_util


def get_auth_token(username) -> dict:
    account: User = get_user(username)

    if not account.is_active():
        raise Exception('This account is not active on our system.')

    jwt_token = jwt_util.create_token(account.user_id, username)

    return {'token': jwt_token}


def create_user(json) -> User:
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(json, 'createAccountHidden')):
        raise Exception('Invalid')

    account_data = get_user_from_json(json, False)
    errors = account_data.validate(False)

    if errors:
        raise Exception(errors)

    user_repo.create_user(account_data)

    return account_data


def delete_user(username):
    if validation_util.is_none_empty_or_zero(username):
        raise Exception('No username found')

    account_data = user_repo.get_user_by_username(username)

    if account_data is None:
        raise Exception(f"Cannot find account for username: {username}")

    # delete account and users in one transaction
    user_repo.delete_user(username)

    return account_data


def disable_user(username):
    user_repo.disable_user(username)


def update_user(json, username):
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(json, 'createAccountHidden')):
        raise Exception('Invalid')

    account_data: User = get_user_from_json(json, True)
    existing_account: User = get_user(username)
    existing_account.update(account_data)
    errors = existing_account.validate(True)

    if errors:
        raise Exception(errors)

    user_repo.update_user(existing_account)

    return existing_account


def get_user_list() -> [dict]:
    account_list: [User] = user_repo.get_user_list()
    account_list_response: [dict] = [account_data.to_json_include_id() for account_data in account_list]
    return account_list_response


def get_user(username) -> User:
    account_data: User = user_repo.get_user_by_username(username)

    if account_data is None:
        raise Exception(f'"Cannot find account for username: {username}')

    return account_data


def get_user_by_id(id) -> User:
    account_data: User = user_repo.get_user_by_id(id)

    if account_data is None:
        raise Exception(f'"Cannot find account')

    return account_data


def get_user_from_json(data, is_update) -> User:
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(data, 'createAccountHidden')):
        raise Exception('Invalid')

    try:
        username = json_util.parse_json(data, 'email_address')
        contact_number = json_util.parse_json(data, 'contact_number')
        email_address = json_util.parse_json(data, 'email_address')
        password = json_util.parse_json(data, 'password')
        account_name = json_util.parse_json(data, 'account_name')
        status = json_util.parse_json(data, 'status')
        status_id = __resolve_account_status_id(status, is_update)

        if validation_util.is_none_empty_or_zero(username):
            username = email_address
        if validation_util.is_none_empty_or_zero(account_name):
            account_name = email_address

        return User(username, password, email_address, status_id)

    except Exception as e:
        raise Exception(str(e))


def __resolve_account_status_id(status, is_update) -> int:
    # if no status found and is not an update
    if validation_util.is_none_empty_or_zero(status) and not is_update:
        return constants.MODEL_STATUS_ACTIVE

    # if validation_util.is_none_empty_or_zero(status):
    #     return 0
    #
    # # if there is a status try and resolve the status id
    # if status in constants.MODEL_STATUS_MAP:
    #     return constants.MODEL_STATUS_MAP[status]

    return 0
