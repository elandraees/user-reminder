from datetime import datetime, timedelta

db_date_format = '%Y-%m-%d %H:%M:%S'
basic_date_format = '%Y-%m-%d'
time_date_format = '%Y-%m-%dT%H:%M'
date_format = '%Y-%m-%d %H:%M'


def get_string_datetime(date: datetime, new_format) -> str:
    return date.strftime(new_format)


def get_datetime(date_string, date_format) -> datetime:
    return datetime.strptime(date_string, date_format)


def now_string() -> str:
    return datetime.now().strftime(db_date_format)


def get_start_of_next_month() -> datetime:
    dt = datetime.now()
    return (dt.replace(day=1) + timedelta(days=32)).replace(day=1).replace(microsecond=0)
