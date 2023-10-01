from datetime import datetime


def now_is():
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return now
