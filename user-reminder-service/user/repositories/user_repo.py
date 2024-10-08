from util.database_util import insert_or_update_db_record, get_query_results, get_query_result
import util.encryption_util as encryption_util
from user.models.user import User
import util.constants as constants

account_insert_column_order = "(username, password, " \
                              "email_address, status_id, create_date, last_update)"

account_load_column_order = "user_id, username, password, " \
                            "email_address, status_id, create_date, last_update"


def create_user(user_data: User, cursor=None, db_connector=None):
    account_insert_value_order = (user_data.username,
                                  encryption_util.get_hashed_salt_value(user_data.password),
                                  user_data.email_address,
                                  user_data.status_id, user_data.create_date, user_data.last_update)

    sql = "INSERT INTO users " + account_insert_column_order + " VALUES (%s, %s, %s, %s, %s, %s)"
    print(sql)
    insert_or_update_db_record(sql, account_insert_value_order, cursor, db_connector)


def get_user_list() -> [User]:
    sql = "SELECT " + account_load_column_order + " from users "
    results = get_query_results(sql, (), None, None)
    if results is None or len(results) == 0:
        return []

    accounts = []
    for result in results:
        account_data = _get_user(result)
        accounts.append(account_data)

    return accounts


def get_user_by_username(username, cursor=None, db_connector=None) -> User | None:
    sql = "SELECT " + account_load_column_order + " from users WHERE username = %s"
    result = get_query_result(sql, (username,), cursor, db_connector)
    return _get_user(result)


def get_user_by_id(user_id, cursor=None, db_connector=None) -> User | None:
    sql = "SELECT " + account_load_column_order + " from users WHERE user_id = %s"
    result = get_query_result(sql, (user_id,), cursor, db_connector)
    return _get_user(result)


def get_user_by_email(email_address, cursor=None, db_connector=None) -> User | None:
    sql = "SELECT " + account_load_column_order + " from users WHERE email_address = %s"
    result = get_query_result(sql, (email_address,), cursor, db_connector)
    return _get_user(result)


def delete_user(username, cursor=None, db_connector=None):
    sql = "DELETE from users where username = %s"
    insert_or_update_db_record(sql, (username,), cursor, db_connector)


def disable_user(username, cursor=None, db_connector=None):
    sql = "UPDATE users set status_id = %s where username = %s"
    insert_or_update_db_record(sql, (constants.MODEL_STATUS_TERMINATED, username), cursor, db_connector)


def update_user(account_data: User, cursor=None, db_connector=None):
    sql = "UPDATE users set email_address = %s," \
          " password= %s, status_id = %s, last_update = %s where username = %s"
    val = (account_data.email_address,
           encryption_util.get_hashed_salt_value(account_data.password),
           account_data.status_id, account_data.last_update, account_data.username)
    insert_or_update_db_record(sql, val, cursor, db_connector)


def _get_user(sql_result) -> User | None:
    if sql_result is None:
        return None

    db_id = sql_result[0]
    username = sql_result[1]
    password = sql_result[2]
    email_address = sql_result[3]
    status_id = sql_result[4]
    create_date = sql_result[5]
    last_update = sql_result[6]

    return User(username, password, email_address, status_id,
                create_date, last_update, db_id)
