import util.validation_util as validation_util
import util.date_util as date_util
import util.constants as constants
from dataclasses import dataclass
import datetime
import user.repositories.user_repo as user_repo


@dataclass
class User:
    username: str
    password: str
    email_address: str
    status_id: int
    create_date: datetime = date_util.now_string()
    last_update: datetime = date_util.now_string()
    user_id: int = 0
    billing_customer_id: int = 0

    def update(self, account_data):
        self.password = self.password if validation_util.is_none_empty_or_zero(account_data.password) \
            else account_data.password

        self.email_address = self.email_address if validation_util.is_none_empty_or_zero(account_data.email_address) \
            else account_data.email_address

        self.status_id = self.status_id if validation_util.is_none_empty_or_zero(account_data.status_id) \
            else account_data.status_id

        self.last_update = date_util.now_string()

    def validate(self, is_update):
        error_dict = {}

        if (validation_util.is_none_empty_or_zero(self.email_address)) \
                or (not validation_util.is_valid_email(self.email_address)):
            error_dict["email_address"] = "Please check email address field is not empty and is a valid email address."

        if self.status_id < 0:
            error_dict["status"] = "Please specify a valid status."

        errors = validation_util.check_password(self.password)
        if len(errors) > 0:
            error_dict["password"] = '\n'.join(errors)

        if is_update:
            return error_dict

        try:
            self.__check_duplicate()
        except Exception as e:
            error_dict["duplicate_account"] = str(e)

        return error_dict

    def __check_duplicate(self):
        account = user_repo.get_user_by_username(self.username)

        if account:
            raise Exception("Account exists for username/email")

        account = user_repo.get_user_by_email(self.email_address)

        if account:
            raise Exception("Account exists for email address.")

    def resolve_status(self):
        return constants.MODEL_STATUS_MAP_ID[self.status_id]

    def is_active(self) -> bool:
        return self.status_id == constants.MODEL_STATUS_ACTIVE

    def to_json(self):
        return { "email_address": self.email_address,
                "status": self.resolve_status(),
                "create_date": self.create_date, "last_update": self.last_update}

    def to_json_include_id(self):
        return {"user_id": self.user_id,
                "email_address": self.email_address, "status": self.resolve_status(), "username": self.username,
                "create_date": self.create_date, "last_update": self.last_update}

