from flask import Blueprint
from util import json_util
from util.controller_helper import *
from reminder.models.reminder import Reminder
import reminder.services.reminder_service as reminder_service

reminder_bp = Blueprint('reminder', __name__, url_prefix='/reminder')


@reminder_bp.route('/create', methods=['POST'])
@authenticate_token
def create_reminder():
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)

    try:
        reminder: Reminder = reminder_service.create_reminder(json, get_user_id())
        return api_response.get_success_response("Successfully reminder", reminder.to_json())
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@reminder_bp.route('/list', methods=['GET'])
@authenticate_token
def get_all_reminders():
    try:
        reminders = reminder_service.get_reminders_for_account_id(get_user_id())
        return api_response.get_success_response("", reminders)
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@reminder_bp.route('/', methods=['GET'])
@authenticate_token
def get_reminders_for_date():
    reminder_date = request.args.get('reminder_date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if (not reminder_date) and (not start_date and not end_date):
        return api_response.get_error_response("No date found", [], 400)

    try:
        reminders = []

        if reminder_date:
            reminders = reminder_service.get_reminders_for_account_id_and_date(get_user_id(), reminder_date)
        elif start_date and end_date:
            reminders = reminder_service.get_reminders_for_account_id_and_date_range(get_user_id(),
                                                                                     start_date, end_date)
        return api_response.get_success_response("", reminders)
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)


@reminder_bp.route('/remove', methods=['POST'])
@authenticate_token
def delete_reminder():
    json = request.json
    if json is None:
        return api_response.get_error_response("No body found", [], 400)
    reminder_id = json['reminder_id']
    if not reminder_id or not reminder_id.isnumeric() or int(reminder_id) <= 0:
        return api_response.get_error_response("Invalid reminder Id specified", [], 400)

    try:
        reminder_service.delete_reminder(int(reminder_id), get_user_id())
        return api_response.get_success_response("Successfully removed reminder", "")
    except Exception as e:
        return api_response.get_error_response("An error has occurred", json_util.parse_str_to_json(str(e)), 400)
