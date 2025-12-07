"""
Utility functions and helpers for the flight booking system.
"""

import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if email is valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.

    Args:
        phone: Phone number to validate

    Returns:
        True if phone is valid, False otherwise
    """
    # Simple validation: at least 10 digits
    digits = "".join(c for c in phone if c.isdigit())
    return len(digits) >= 10


def validate_date_format(date_str: str, format: str = "%Y-%m-%d") -> bool:
    """
    Validate date string format.

    Args:
        date_str: Date string to validate
        format: Expected date format (default: YYYY-MM-DD)

    Returns:
        True if date is valid, False otherwise
    """
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def generate_id(prefix: str, sequence: int) -> str:
    """
    Generate a unique ID with given prefix.

    Args:
        prefix: ID prefix
        sequence: Sequential number

    Returns:
        Generated ID
    """
    return f"{prefix}-{sequence:06d}"


def calculate_age(date_of_birth_str: str) -> int:
    """
    Calculate age from date of birth.

    Args:
        date_of_birth_str: Date of birth in YYYY-MM-DD format

    Returns:
        Age in years
    """
    try:
        dob = datetime.strptime(date_of_birth_str, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )
        return age
    except ValueError:
        return 0


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format amount as currency string.

    Args:
        amount: Amount to format
        currency: Currency code (default: USD)

    Returns:
        Formatted currency string
    """
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "PKR": "Rs.",
    }
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol} {amount:,.2f}"


def get_seat_number_range(start_seat: str, end_seat: str) -> list:
    """
    Generate seat number range.

    Args:
        start_seat: Start seat number (e.g., "1A")
        end_seat: End seat number (e.g., "1F")

    Returns:
        List of seat numbers in range
    """
    # Extract row number and column letter
    start_row = int("".join(c for c in start_seat if c.isdigit()))
    start_col = "".join(c for c in start_seat if c.isalpha())

    end_row = int("".join(c for c in end_seat if c.isdigit()))
    end_col = "".join(c for c in end_seat if c.isalpha())

    if start_row != end_row:
        raise ValueError("Start and end seats must be in the same row")

    seats = []
    current_col = ord(start_col)
    end_col_ord = ord(end_col)

    while current_col <= end_col_ord:
        seats.append(f"{start_row}{chr(current_col)}")
        current_col += 1

    return seats
