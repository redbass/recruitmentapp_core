from lib.password import encrypt_user_password, check_user_password
from test import UnitTestCase


class TestPasswordEncryption(UnitTestCase):

    def test_password_encryption_decryption(self):

        password = 'some_password'
        hashed_password = encrypt_user_password(password)
        self.assertTrue(check_user_password(password=password,
                                            hashed=hashed_password))
