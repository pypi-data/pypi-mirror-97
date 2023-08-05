import datetime


def current_time_str():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
