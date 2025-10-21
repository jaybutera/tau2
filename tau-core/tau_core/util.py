#!/usr/bin/env python3
"""Shared utility functions for tau tools"""
import random
import time
from datetime import datetime


def random_blob_idx():
    """Generate random blob index for task storage"""
    return "%030x" % random.randrange(16**30)


def datetime_to_unix(dt):
    """Convert datetime to unix timestamp"""
    return int(time.mktime(dt.timetuple()))


def now():
    """Get current unix timestamp"""
    return datetime_to_unix(datetime.now())


def current_month():
    """Get current month in MMYY format"""
    today = datetime.today()
    return today.strftime("%m%y")


def unix_to_datetime(timestamp):
    """Convert unix timestamp to datetime"""
    return datetime.utcfromtimestamp(timestamp)


def today():
    """Get today's date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")


def parse_hours(hours_str):
    """Parse hour string like '4h' or '4' to int"""
    if hours_str.endswith('h'):
        return int(hours_str[:-1])
    return int(hours_str)


def format_date(date_str):
    """Format date for display"""
    return date_str


# Task template for validation
task_template = {
    "blob_idx": str,
    "assigned": list,
    "title": str,
    "desc": str,
    "tags": list,
    "project": str,
    "status": str,
    "rank": float,
    "due": int,
    "created": int,
    "events": list,
}


def enforce_task_format(task):
    """Validate task format against template"""
    for attr, val in task.items():
        val_type = task_template[attr]
        if val is None:
            assert val_type == list or attr not in ["blob_idx", "created"]
            continue
        assert isinstance(val, val_type)
