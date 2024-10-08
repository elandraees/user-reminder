from reminder.models.reminder import Reminder
import util.date_util as date_util
from util.database_util import insert_or_update_db_record, get_query_results, get_query_result, insert_return_id
import datetime

reminder_insert_column_order = "(user_id, note, reminder_date)"

reminder_load_column_order = "reminder_id, user_id, note, reminder_date"


def create_reminder(reminder: Reminder) -> int:
    insert_value_order = (reminder.user_id, reminder.note, reminder.reminder_date)

    sql = "INSERT INTO reminders " + reminder_insert_column_order + "VALUES (%s, %s, %s) RETURNING reminder_id"
    return insert_return_id(sql, insert_value_order)


def get_reminders_by_account_id(user_id: int) -> [Reminder]:
    sql = "SELECT " + reminder_load_column_order + " from reminders where user_id = %s"
    results = get_query_results(sql, (user_id,), None, None)
    if results is None or len(results) == 0:
        return []

    reminders = []
    for result in results:
        reminder_data = _get_reminder(result)
        reminders.append(reminder_data)

    return reminders


def get_reminders_by_account_id_and_date(user_id: int, date: datetime):
    sql = "SELECT " + reminder_load_column_order + " from reminders where user_id = %s and reminder_date >= %s " \
                                                   "and reminder_date < %s "
    print(sql, user_id, date)
    results = get_query_results(sql, (
    user_id, date, datetime.datetime.strptime(date, date_util.time_date_format) + datetime.timedelta(days=1)), None,
                                None)
    if results is None or len(results) == 0:
        return []

    reminders = []
    for result in results:
        reminder_data = _get_reminder(result)
        reminders.append(reminder_data)

    return reminders


def get_reminders_by_account_id_and_date_range(user_id: int, start_date: datetime, end_date: datetime):
    sql = "SELECT " + reminder_load_column_order + " from reminders where user_id = %s and reminder_date >= %s " \
                                                   "and reminder_date < %s "
    results = get_query_results(sql, (user_id, start_date, end_date), None, None)
    if results is None or len(results) == 0:
        return []

    reminders = []
    for result in results:
        reminder_data = _get_reminder(result)
        reminders.append(reminder_data)

    return reminders


def _get_reminder(sql_result) -> Reminder | None:
    if sql_result is None:
        return None

    db_id = sql_result[0]
    account_id = sql_result[1]
    note = sql_result[2]
    reminder_date = sql_result[3]

    return Reminder(account_id, reminder_date, note, db_id)


def delete_reminder(reminder_id:int, user_id:int):
    sql = 'delete from reminders where reminder_id = %s and user_id = %s'
    insert_or_update_db_record(sql, (reminder_id, user_id))
