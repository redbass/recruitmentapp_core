import os
from Crypto.Cipher import AES


class BaseConfig(object):

    ENC_SEED = 'aaaaaaaaaaaaaaaa'
    ENC_PSWD = None

    DEBUG = False
    DEFAULT_PORT = None

    DATABASE_HOST = ''
    DATABASE_PORT = None
    DATABASE_USER = None
    DATABASE_PASSWORD = None
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
