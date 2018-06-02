import re


def validate_email(email):
    r = '[^@]+@[^@]+\.[^@]+'
    return re.match(r, email) is not None
