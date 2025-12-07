"""
Helper functions for the flight booking system.
"""

from datetime import datetime


def get_current_timestamp() -> datetime:
    """
    Get current timestamp.

    Returns:
        Current datetime
    """
    return datetime.now()


def is_within_date_range(
    date_str: str, start_date_str: str, end_date_str: str
) -> bool:
    """
    Check if a date falls within a date range.

    Args:
        date_str: Date to check
        start_date_str: Start of range
        end_date_str: End of range

    Returns:
        True if date is within range
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        return start_date <= date <= end_date
    except ValueError:
        return False


def calculate_days_until(target_date_str: str) -> int:
    """
    Calculate days until a target date.

    Args:
        target_date_str: Target date in YYYY-MM-DD format

    Returns:
        Number of days until target date (negative if date is in past)
    """
    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
        today = datetime.now()
        delta = target_date - today
        return delta.days
    except ValueError:
        return 0


def is_peak_hour(hour: int) -> bool:
    """
    Check if given hour is during peak hours.

    Args:
        hour: Hour (0-23)

    Returns:
        True if hour is peak hour
    """
    return hour in [6, 7, 8, 9, 17, 18, 19, 20]


def is_holiday(month: int, day: int) -> bool:
    """
    Check if given date is a holiday (simplified).

    Args:
        month: Month (1-12)
        day: Day (1-31)

    Returns:
        True if date is a holiday
    """
    # Simplified holiday check
    holidays = [
        (1, 1),  # New Year
        (7, 4),  # Independence Day (US)
        (12, 25),  # Christmas
    ]
    return (month, day) in holidays
