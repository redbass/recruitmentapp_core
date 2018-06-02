from lib.password import encrypt_password, check_password
from test import UnitTestCase


class TestPasswordEncryption(UnitTestCase):

    def test_password_encryption_decryption(self):

        password = 'some_password'
        hashed_password = encrypt_password(password)
        self.assertTrue(check_password(password=password,
                                       hashed=hashed_password))
