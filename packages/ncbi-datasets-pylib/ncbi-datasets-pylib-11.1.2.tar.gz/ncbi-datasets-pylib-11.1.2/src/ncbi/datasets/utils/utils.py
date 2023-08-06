import datetime


def get_iso8601_datetime():
    return datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
