from dataclasses import dataclass
import datetime
import util.validation_util as validation_util
import util.date_util as date_util


@dataclass
class Reminder:
    user_id: int
    reminder_date: datetime
    note: str
    reminder_id: int = 0

    def validate(self):
        error_dict = {}

        if validation_util.is_none_empty_or_zero(self.reminder_date):
            error_dict["reminder_date"] = "No reminder date specified"

        if self.reminder_date < datetime.datetime.now():
            error_dict["reminder_date"] = "Please specify a future date"

        if validation_util.is_none_empty_or_zero(self.note):
            error_dict["note"] = "No reminder note specified"

        return error_dict

    def to_json(self):
        return {
            "reminder_date": date_util.get_string_datetime(self.reminder_date,
                                                           date_util.time_date_format),
            "note": self.note,
            "user_id": self.user_id,
            "reminder_id": self.reminder_id
        }

