import bcrypt

from config import settings


def encrypt_password(password):
    utf8_password = password.encode('UTF-8')
    return bcrypt.hashpw(utf8_password, settings.SALT)


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('UTF-8'), hashed)
