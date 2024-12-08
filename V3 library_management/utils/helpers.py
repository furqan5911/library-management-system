# Helper functions
# Helper functions

from datetime import datetime


def format_date(date):
    """
    Formats a datetime object into a readable string.
    """
    return date.strftime("%Y-%m-%d %H:%M:%S")


def print_separator():
    """
    Prints a separator line for better readability in the console output.
    """
    print("=" * 50)


def parse_float(value):
    """
    Parses a value into a float, ensuring safe conversion.
    """
    try:
        return float(value)
    except ValueError:
        return None


def get_user_full_name(user):
    """
    Returns the full name of a user from a dictionary object.
    """
    return f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
