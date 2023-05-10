from datetime import datetime


def get_timestamp():
    return datetime.now().timestamp()


def get_curr_time():
    return datetime.now().time()