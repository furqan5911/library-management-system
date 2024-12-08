# Validation utilities
# Validation utilities

import re


def validate_email(email):
    """
    Validates if the provided email address has a valid format.
    """
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(email_regex, email):
        return True
    return False


def validate_password(password):
    """
    Validates if the provided password is strong.
    - At least 8 characters long.
    - Contains at least one uppercase letter.
    - Contains at least one number.
    - Contains at least one special character.
    """
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+{}[]|:;'<>?,./" for char in password):
        return False
    return True
