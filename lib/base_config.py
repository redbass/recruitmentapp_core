import os
from datetime import timedelta

from Crypto.Cipher import AES


class BaseConfig(object):

    ENC_SEED = 'aaaaaaaaaaaaaaaa'
    ENC_PSWD = None

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=60)

    DEBUG_MODE = False
    TEST = False
    DEFAULT_PORT = None

    LOGIN_REQUIRED = True
    API_TOKEN_REQUIRED = True

    DATABASE_HOST = ''
    DATABASE_PORT = None
    DATABASE_USER = None
    DATABASE_PASSWORD = None
    DATABASE_NAME = None
    DATABASE_DB_SUFFIX = ''

    def __init__(self):
        self.ENC_PSWD = os.environ.get('ENC_PSWD', None)

        if self.DATABASE_PASSWORD:
            self.DATABASE_PASSWORD = self.decrypt(self.DATABASE_PASSWORD)

    def encrypt(self, msg: str):
        aes = AES.new(self.ENC_PSWD, AES.MODE_CBC, self.ENC_SEED)
        return aes.encrypt(msg).hex()

    def decrypt(self, cipher_hex: str):
        b_cipher_hex = bytes(bytearray.fromhex(cipher_hex))
        aes = AES.new(self.ENC_PSWD, AES.MODE_CBC, self.ENC_SEED)
        return aes.decrypt(b_cipher_hex).decode()
