import time
import datetime
import math


def format_time_since_epoch(seconds):
    currentTime = int(time.time())
    seconds_since_created = currentTime - seconds

    if seconds_since_created < 60:
        return f"{seconds_since_created}s"

    minutes_since_created = math.floor(seconds_since_created / 60)
    if minutes_since_created < 60:
        return f"{minutes_since_created}m"

    hours_since_created = math.floor(minutes_since_created / 60)
    if hours_since_created < 24:
        return f"{hours_since_created}h"

    return datetime.datetime.fromtimestamp(seconds_since_created).strftime("%d %b")
