from reminder.models.reminder import Reminder
import util.validation_util as validation_util
import util.json_util as json_util
import util.date_util as date_util
import reminder.repositories.reminder_repo as reminder_repo
import datetime


def create_reminder(json, account_id) -> Reminder:
    reminder: Reminder = get_reminder_from_json(json, account_id)

    errors = reminder.validate()

    if errors:
        raise Exception(errors)

    reminder_id = reminder_repo.create_reminder(reminder)
    reminder.reminder_id = reminder_id
    return reminder


def delete_reminder(reminder_id, user_id):
    reminder_repo.delete_reminder(reminder_id, user_id)


def get_reminders_for_account_id(account_id) -> [dict]:
    reminder_list: [Reminder] = reminder_repo.get_reminders_by_account_id(account_id)
    return [reminder.to_json() for reminder in reminder_list]


def get_reminders_for_account_id_and_date(account_id: int, date: datetime) -> [dict]:
    reminder_list: [Reminder] = reminder_repo.get_reminders_by_account_id_and_date(account_id, date)
    return [reminder.to_json() for reminder in reminder_list]


def get_reminders_for_account_id_and_date_range(account_id: int, start_date: datetime, end_date: datetime) -> [dict]:
    reminder_list: [Reminder] = reminder_repo.get_reminders_by_account_id_and_date_range(account_id,
                                                                                         start_date, end_date)
    return [reminder.to_json() for reminder in reminder_list]


def get_reminder_from_json(data, account_id) -> Reminder:
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(data, 'createAccountHidden')):
        raise Exception('Invalid')

    try:
        reminder_date_string = json_util.parse_json(data, 'reminder_date')

        try:
            reminder_date = date_util.get_datetime(reminder_date_string, date_util.time_date_format)
        except Exception as e:
            raise Exception(f"Please specify the date in the format {date_util.time_date_format}")

        note = json_util.parse_json(data, 'note')
        return Reminder(account_id, reminder_date, note)

    except Exception as e:
        raise Exception(str(e))
