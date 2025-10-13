#!/usr/bin/env python3
from datetime import datetime

def parse_hours(hours_str):
    """Parse hour string like '4h' or '4' to int"""
    if hours_str.endswith('h'):
        return int(hours_str[:-1])
    return int(hours_str)

def format_date(date_str):
    """Format date for display"""
    return date_str

def today():
    return datetime.now().strftime("%Y-%m-%d")
