import re


def validate_email(email):
    r = r'[^@]+@[^@]+\.[^@]+'
    return re.match(r, email) is not None
