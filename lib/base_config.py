import os
from datetime import timedelta

from lib.password import decrypt_system_password, encrypt_system_password


class BaseConfig(object):

    ENC_SEED = 'this_is_not_a_seed'
    ENC_PSWD = os.environ.get('ENC_PSWD', None)

    MAX_CONTENT_LENGTH = 400000
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    DEFAULT_API_KEY = os.environ.get('DEFAULT_API_KEY')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=60)

    DEBUG_MODE = False
    TEST = False
    DEFAULT_PORT = None

    LOGIN_REQUIRED = True
    API_TOKEN_REQUIRED = True

    DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', None)
    DATABASE_PORT = os.environ.get('DATABASE_PORT', '27017')
    DATABASE_USER = os.environ.get('DATABASE_USER', None)
    DATABASE_NAME = os.environ.get('DATABASE_NAME', None)
    DATABASE_DB_SUFFIX = ''

    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', None)
    SENDGRID_SECRET_KEY = os.environ.get('SENDGRID_SECRET_KEY', None)

    def __init__(self):
        if self.DATABASE_PASSWORD:
            self.DATABASE_PASSWORD = self.decrypt(self.DATABASE_PASSWORD)

    def encrypt(self, password: str):
        return encrypt_system_password(password, self.ENC_PSWD, self.ENC_SEED)

    def decrypt(self, hex: str):
        return decrypt_system_password(hex, self.ENC_PSWD, self.ENC_SEED)
